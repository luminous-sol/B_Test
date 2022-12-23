from django.urls import path
from . import views # 현재 디렉토리 안에서 views  import

urlpatterns = [
    # path('', views.index),
    # blog에 urls파일로 왔다. 
    # views 파일에 index 로 가는 길을 알려줌 
    # views.py 의 index 함수를 PostList 클래스로 대체했기 때문에 지워준다. 
    # /blog 뒤에 아무것도 안 붙이면 여기로 넘어온다. 
    
    path('', views.PostList.as_view()),
    # PostList를 쓰면 template으로 갈 땐 post_list.html으로 간다. 
    
    path('<int:pk>/', views.PostDetail.as_view()),
    # blog /n 붙어서 페이지(순서)나오게
    
    path('category/<str:slug>/',views.category_page),
    # blog/urls.py 에 링크 걸 path 추가
    
    path('tag/<str:slug>/',views.tag_page),
    # slug로 들어온다. tag_page는 이제 만들 예정
    
    path('create_post/', views.PostCreate.as_view()),
    
    path('<int:pk>/new_comment/',views.new_comment),
    
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()), # 댓글 수정 업데이트 
    # CommentUpdate만들어주기

    path('delete_comment/<int:pk>/',views.delete_comment),
    
    path('search/<str:q>/',views.PostSearch.as_view()), #Search Widget 
]