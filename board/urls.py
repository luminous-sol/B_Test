from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.BoardCreate.as_view()),
    # 크리에이크 경로로 들어오면 views 파일에 들어가서 BoardCreate 클래스 찾아서 실행하라
    path('<int:pk>/', views.BoardDetail.as_view()),
    # 보드 pk 받아서 숫자 들어가면 보드 내용 나오게 만들기
    path('', views.BoardList.as_view()),
    # board창에 들어갔을 때 보드 게시글 리스트 나타내기
]