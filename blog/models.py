from django.db import models

# def (힘수)사용해서 작성하는 방법

# class 사용해서 작성하는 방법
class Post(models.Model):
    title = models.CharField(max_length = 70)
    # 제목 최대 길이
    content = models.TextField()
    # 콘텐츠는 텍스트필드불러온다(글적는 칸)
    
    create_at = models.DateTimeField(auto_now_add=True)
    # 날짜 작성하는 이름
    updated_at = models.DateTimeField(auto_now=True)
    # 현재 시간으로 알아서 세팅되도록 한다. auto_now 추가
    
    def __str__(self) :
        return f'[{self.pk}]{self.title}'
        # Post object(1) 이렇게 표시되는 콘텐츠를 제목이 나오도록 변경시켜준다. 
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
# Create your models here.
# models.py 수정 후에는 무조건 migration 해주어야 한다. 