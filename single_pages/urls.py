from django.urls import path
from . import views 

urlpatterns = [
    path('about_me/', views.about_me),
    # about_me라는 path를 urls을 얻어올거다. views 에서
    path('', views.landing)
    # views에서 about_me 와 landing 을 받아 올 것이다. 
    # 현재 디렉토리의 views에서 import 하라고 하였으므로 views에 가본다. 
    # 하지만 views에는 아무것도 존재하지 않기 때문에 다음과 같이 입력해준다. 
]