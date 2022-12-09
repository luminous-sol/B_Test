from django.contrib import admin
from .models import Post 

admin.site.register(Post)
# Register your models here.
# admin 페이지에 Post 기능(제목 / 콘텐츠글쓰기 / 날짜불러오기)추가