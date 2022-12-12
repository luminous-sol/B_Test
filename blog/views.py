from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post 

class PostList(ListView):
    model = Post 
    ordering = '-pk'
    # ListView = Post 나열 밑에 선언해뒀던 index 함수의 역할을 한다. 
    # def get_context_data(self, **kwargs):
    #     context = super(PostList, self).get_context_data()
    #     context['categories'] = Category.objects.all()
    #     context['no_category_post_count'] = Post.context.filter(category=None).count()
    #     return context

class PostDetail(DetailView):
    model = Post 
    # 함수 single_post_page 대체

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