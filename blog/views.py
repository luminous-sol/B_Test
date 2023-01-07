from django.shortcuts import render, redirect, get_object_or_404 
# object 를 받아들이거나 404 
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.text import slugify
from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from .models import Post , Category , Tag, Comment
from django.db.models import Q


class PostCreate(CreateView, LoginRequiredMixin, UserPassesTestMixin): # 로그인이 요구된다
    model = Post 
    fields = ['title', 'hook_text','content','head_image','file_upload','category','tag']
    # 포스트 작성 화면에서 보여줄 필드명들을 적어주기
    # 로그인 한 후 보여주는 작성 화면이니까 작성자가 굳이 들어갈 필요 없음
    # 작성 시간도 자동으로 설정되니까 필요 없음
    # 태그는 사용자가 직접 추가하는 형식으로
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            
            response = super(PostCreate,self).form_valid(form)
            
            tag_str = self.request.POST.get('tag_str')
            if tag_str:
                tag_str = tag_str.strip()
                tag_str = tag_str.replace(',',';')
                tag_list = tag_str.split(';')
                
                for t in tag_list :
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                                                # 있으면 불러오고 없으면 생성한다.
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tag.add(tag)
            
            return response
        else:
            return redirect('/blog/')
        

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post 
    fields = ['title', 'hook_text','content','head_image','file_upload','category','tag']
    
    template_name = 'blog/post_update_form.html'
    # blog에 post_update_form으로 찾아가기
    # 없으니까 만들어 줄 것
    
    def get_context_data(self, **kwargs):
        context = super(PostUpdate,self).get_context_data()
        if self.object.tag.exists():
            tag_str_list = list()
            for t in self.object.tag.all():
                tag_str_list.append(t.name)
            context['tag_str_default'] = ';'.join(tag_str_list)
        return context
    
    def form_valid(self, form):
        response = super(PostUpdate,self).form_valid(form)
        self.object.tag.clear()
            
        tag_str = self.request.POST.get('tag_str')
        if tag_str:
            tag_str = tag_str.strip()
            tag_str = tag_str.replace(',',';')
            tag_list = tag_str.split(';')
                
            for t in tag_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                                            # 있으면 불러오고 없으면 생성한다.
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tag.add(tag)
            
        return response
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author :
            # 지금 로그인 되어 있는 사용자가 인증되었는지
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied
            # 인증이 안되었으면 권한이 거절된다.  

            
class PostList(ListView):
    model = Post
    ordering = '-pk'
    paginate_by = 5
    # ListView = Post 나열 밑에 선언해뒀던 index 함수의 역할을 한다. 
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post
    ordering = '-pk'
    # 함수 single_post_page 대체
    
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        # super가 상위 PostList의 model가 ordering을 불러 올 수 있다. 
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        
        context['comment_form'] = CommentForm
        
        return context
    
class PostSearch(PostList): # 포스트 검색은 포스트 작성 후 이루어 져야 하므로 Post~ 의 클래스가 끝난 후 구현해준다. 
    paginate_by = None # 검색결과 다 보여줘class PostSearch(PostList): # 포스트 검색은 포스트 작성 후 이루어 져야 하므로 Post~ 의 클래스가 끝난 후 구현해준다. 
    
    def get_queryset(self): # DB에서 찾아오기
        q = self.kwargs['q']
        post_list =Post.objects.filter(
            Q(title__contains = q) | Q(tag__name__contains = q) | Q(content__contains = q)
        ).distinct() # DB에서 중복 피하는 것 (제목이 q를 포함하고 있거나 태그 이름이 q를 포함하거나) distinct(): 배열 중복값을 제거한다.  
        return post_list # 타이틀과 태그에서 찾은 중복없는 자료를 넘겨준다.
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q'] 
        context['search_info'] = f'Search : {q} ({ self.get_queryset().count() })' # 검색 결과 개수 표시
        
        return context
    


    
    
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author : # 승인된 관리자이고 작성자랑 동일하면
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs) # 코멘트 업데이트
        else :
            raise PermissionDenied # 아니면 승인 거절
    
    
def category_page(request,slug):
    if slug == 'no_category':
        category = "미분류"
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
        
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
     )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list':post_list,
            'tag':tag,
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
        }
    )


def new_comment(request, pk) : #댓글 적힐 게시물의 번호 가지고 오기
    if request.user.is_authenticated :
        post = get_object_or_404(Post, pk=pk) # pk가 없을 때 object 가지고 오거나
        if request.method == 'POST': # 포스트 방식으로 들어왔다면 
            comment_form = CommentForm(request.POST)
    
            if comment_form.is_valid() : # 정상적으로 가져왔으면 자료 가져오면 된다
                comment = comment_form.save(commit = False)
                # commit = DB 에 완벽하게 저장해도 된다 것을 알려준다. False >> 저장하지마라
                comment.post = post
                comment.author = request.user 
                comment.save() # 여기서 진짜 저장
                return redirect(comment.get_absolute_url())
        else : # 'GET' : 주소창에 직접 입력해서 들어온 경우
            return redirect(post.get_absolute_url()) # 다시 게시글로 넘겨주기
    else :
        raise PermissionDenied # 승인거절
        
        
def delete_comment (request, pk) :
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post

    if request.user.is_authenticated and request.user == comment.author :
        comment.delete() # 삭제해주기
        return redirect(post.get_absolute_url())
    else:
        return PermissionDenied
    
    
# 함수방법 def 으로 만들기
# 클라이언트에서 넘어온 정보(request) urlpatterns을 타고 views의 index 함수로 넘어옴

# def index(request):
    
#     posts = Post.objects.all()
#     # DB Query 명령어 => DB에 있는 것 모두 가지고 오게 하는 명령어
#     # order_by('-pk') : 오름차순인데 pk순서 거꾸로 나오게 (최근 글부터)
    
#     return render (
#     request,
#     'blog/index.html',
#     {
#         'posts':posts,
#         # class Post() 클래스 방식 models.py 
#     }
#     )
#     # render() 는 blog template을 찾으러 간다.
    
#     # template 안에 blog 안에 index.html을 만들어 request를 수행한다. 
#     # request 는 blog방 안의 index.html으로 보낸다. 
    
# def single_post_page(request, pk):
        
#     post = Post.objects.get(pk=pk)
#     # blog/n 해서 pk = n 이 들어오면 pk=pk 해서 DB.get(n)
        
#     return render (
#     request,
#     'blog/single_post_page.html',
#     {
#         'post':post,
#     }
# )