from django.db import models
from django.contrib.auth.models import User
import os
# def (힘수)사용해서 작성하는 방법


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # slugfield = 사람이 읽을 수 있는 텍스트로 고유의 url 생성 => 가독성 높여준다. 
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
    
    class Meta :
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'
        
        
# class 사용해서 작성하는 방법
class Post(models.Model):
    title = models.CharField(max_length = 70)
    # 제목 최대 길이
    hook_text = models.CharField(max_length = 100, blank = True)
    # admin에서 hook_text를 넣을 수 있는 공간을 만들어 주자
    content = models.TextField()
    # 콘텐츠는 텍스트필드불러온다(글적는 칸)
    
    
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    # 실제로는 _media 방 안에 만들어진다. 
    # blank=True 필수항목이 아니기 때문에 비워도 된다. 
    # 이미지 저장하지 않아도 된다.
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    # 날짜 작성하는 이름
    updated_at = models.DateTimeField(auto_now=True)
    # 현재 시간으로 알아서 세팅되도록 한다. auto_now 추가
    
    author = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    # on_delete = models.CASCADE 작성자 계정 탈퇴하면 게시글도 삭제하겠다. 
    # on_delete = models.SET_NULL 작성자 계정 탈퇴하면 작성자만 none 처리할거다
    category = models.ForeignKey(Category, null = True, blank = True, on_delete= models.SET_NULL)
    # blank=True 하면 카테고리가 비어 있어도 된다. 누락을 수락한다. 카테고리 지워져도 연관된 게시글은 계속 남아있게 한다. 
    
    tags = models.ManyToManyField(Tag, blank = True)
    
    def __str__(self) :
        return f'[{self.pk}]{self.title}::{self.author}'
        # Post object(1) 이렇게 표시되는 콘텐츠를 제목이 나오도록 변경시켜준다.
        
    def get_absolute_url(self):
        return f'/blog/{self.pk}'
    
    # 경로 제외한 파일명 받아오기
    def get_file_name(self): 
        return os.path.basename(self.file_upload.name)
    
    # 확장자 받아오기 / ext = extension 확장자
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
    
