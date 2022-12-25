from django.shortcuts import render
from blog.models import Post

def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    # 끝에서 세 개(역순으로) 최근 게시글가지고 오기

    return render(
    request,
    'single_pages/landing.html',{
        'recent_posts' : recent_posts,
    }
    )

def about_me(request):
    return render(
    request,
    'single_pages/about_me.html'
    )
# single_pages 에서 받아 올 landing.html, about_me.html 파일을 만들어준다. 
# landing.html 이 메인 그리고 about_me.html 이 내부 페이지가 될 예정이다. 