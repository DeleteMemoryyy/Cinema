from django import forms
from .models import Movie
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'score', 'content']
