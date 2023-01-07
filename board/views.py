from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Board
from . forms import BoardForm

# Create your views here.

class BoardCreate(LoginRequiredMixin, CreateView):    
    model = Board 
    form_class = BoardForm
    
    def form_valid(self, form): # 폼 검증
        current_user = self.request.user 
        
        if current_user.is_authenticated : # 만약 현재 유저가 승인되었으면 
            form.instance.author = current_user
            response = super(BoardCreate, self).form_valid(form)
            
            return response
        else :
            return redirect('/board/')
        


class BoardList(ListView):
    model = Board 
    ordering = '-pk'

    
class BoardDetail(DetailView):
    model = Board
    
    

    