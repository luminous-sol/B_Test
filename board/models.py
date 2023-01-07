from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField


class Board(models.Model):
    title = models.CharField(max_length=150)
    
    content = MarkdownxField()
    
    create_at = models.DateTimeField(auto_now_add=True)
    # 날짜 작성하는 이름
    updated_at = models.DateTimeField(auto_now=True)
    # 현재 시간으로 알아서 세팅되도록 한다. auto_now 추가
    
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
# Create your models here.

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}'
    
    def get_absolute_url(self):
        return f'/board/{self.pk}/'
    # 새로운 앱을 추가하