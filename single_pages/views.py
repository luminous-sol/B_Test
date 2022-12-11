from django.shortcuts import render

def landing(request):
    return render(
    request,
    'single_pages/landing.html'
    )

def about_me(request):
    return render(
    request
    'single_pages/about_me.html'
    )
# single_pages 에서 받아 올 landing.html, about_me.html 파일을 만들어준다. 
# landing.html 이 메인 그리고 about_me.html 이 내부 페이지가 될 예정이다. 