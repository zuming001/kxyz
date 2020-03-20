from apps.forms import FormMixin
from apps.news.models import News, Banner
from apps.course.models import Course

from django import forms


class AddNewsCategoryForm(forms.Form, FormMixin):
    name = forms.CharField(error_messages={'required': '必须传入新闻分类的名称! '})


class EditNewsCategoryForm(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={"required": "必须传入新闻分类的id! "})
    name = forms.CharField(max_length=100)


class WriteNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['author', 'pub_time', 'category']


class EditNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()
    pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class AddBannerForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Banner
        fields = ['priority', 'image_url', 'link_to']


class EditBannerForm(forms.ModelForm, FormMixin):
    # 因为id在Banner的模型中没有定义,所以需要我们自己定义id,也就是pk(主键);并且id是一个函数名,不能用作变量
    pk = forms.IntegerField()

    class Meta:
        model = Banner
        fields = ['image_url', 'link_to', 'priority']


class PubCourseForm(forms.ModelForm, FormMixin):
    category_id = forms.IntegerField(error_messages={'required': '必须传入课程分类id'})
    lecturer_id = forms.IntegerField(error_messages={'required': '必须传入讲师id'})

    class Meta:
        model = Course
        exclude = ['category', 'lecturer', 'pub_time']

class AddCourseCtegoryForm(forms.Form,FormMixin):
    name = forms.CharField(error_messages={'required': '新增课程分类名称不为空'})

class EditCourseCategoryForm(forms.Form, FormMixin):
    pk = forms.IntegerField()
    name = forms.CharField(error_messages={'required': '修改后课程分类名称不为空!'})
