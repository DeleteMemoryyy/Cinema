# -*- coding: UTF-8 -*-

from django import forms


class ReviewForm(forms.Form):
    author = forms.CharField(max_length=50, label='作者',)
    score = forms.IntegerField(label='评分')
    content = forms.CharField(max_length=512, label='内容')
