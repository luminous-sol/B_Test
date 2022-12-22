from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post , Category, Tag



admin.site.register(Post)
# Register your models here.
# admin 페이지에 Post 기능(제목 / 콘텐츠글쓰기 / 날짜불러오기)추가

class CategoryAdmin(admin.ModelAdmin):
    # 관리자 페이지에 카테고리 화면 만들기
    prepopulated_fields = {'slug' : ('name', )}
    # name을 입력하면 slug 가 알아서 url을 만들어준다. 


class TagAdmin(admin.ModelAdmin):
    # 관리자 페이지에 Tag 화면 만들기
    prepopulated_fields = {'slug' : ('name', )}
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

