"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
# path 를 사용하기 위해 include import

urlpatterns = [
    path('blog/', include('blog.urls')), 
    #blog에 urls로 가라는 명령 # 있으려면 blog에 urls 파일이 있어야 한다. 
    path('admin/', admin.site.urls),
    
    
    path('', include('single_pages.urls')),
    # single_pages에 urls로 가라는 명령 있으려면 single_pages에 urls 파일이 있어야 한다. 
    path('markdownx/', include('markdownx.urls'))
]
urlpatterns += static(settings.MEDIA_URL,
                     document_root = settings.MEDIA_ROOT)