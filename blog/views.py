from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post , Category , Tag


class PostCreate(CreateView, LoginRequiredMixin): # 로그인이 요구된다
    model = Post 
    fields = ['title', 'hook_text','content','head_image','file_upload','category','tag']
    # 포스트 작성 화면에서 보여줄 필드명들을 적어주기
    # 로그인 한 후 보여주는 작성 화면이니까 작성자가 굳이 들어갈 필요 없음
    # 작성 시간도 자동으로 설정되니까 필요 없음
    # 태그는 사용자가 직접 추가하는 형식으로


class PostList(ListView):
    model = Post 
    ordering = '-pk'
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
        
        return context
    
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