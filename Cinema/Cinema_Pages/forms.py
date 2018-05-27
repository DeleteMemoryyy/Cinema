# -*- coding: UTF-8 -*-

from django import forms


class ReviewForm(forms.Form):
    author = forms.CharField(max_length=50, label='作者', )
    # score = forms.IntegerField(label='评分')
    score = forms.ChoiceField(
        choices=[(1, '1分'), (2, '2分'), (3, '3分'), (4, '4分'), (5, '5分'), (6, '6分'), (7, '7分'), (8, '8分'), (9, '9分'),
                 (10, '10分')])
    content = forms.CharField(widget=forms.Textarea, label='内容')
