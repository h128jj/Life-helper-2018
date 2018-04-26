from django import forms


class PostForm(forms.Form):
    title = forms.CharField(label="title", max_length=100)
    content = forms.CharField(label="content", max_length=10000)