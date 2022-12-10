from django.urls import path
from . import views # 현재 디렉토리 안에서 views  import

urlpatterns = [
    path('', views.index),
    # blog에 urls파일로 왔다. 
    # views 파일에 index 로 가는 길을 알려줌 
    path('<int:pk>/', views.single_post_page),
    # blog /n 붙어서 페이지(순서)나오게
]