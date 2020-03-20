from django import forms
from apps.forms import FormMixin


class PublicCommentForms(forms.Form, FormMixin):
    content = forms.CharField(error_messages={'required':'评论内容不能为空！ '})
    news_id = forms.IntegerField()

