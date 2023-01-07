from .models import Board
from django import forms

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']