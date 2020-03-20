from django import forms
from apps.forms import FormMixin
from django.core.cache import cache
from .models import User


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, error_messages={"error": "账号名已被注册"})
    password = forms.CharField(max_length=10, min_length=6,
                               error_messages={"max_length": "密码不长于10个字符", "min_length": "密码不短于6个字符"})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=10, min_length=6,
                                error_messages={"max_length": "密码不长于10个字符", "min_length": "密码不短于6个字符"})
    password2 = forms.CharField(max_length=10, min_length=6,
                                error_messages={"max_length": "密码不长于10个字符", "min_length": "密码不短于6个字符"})
    img_captcha = forms.CharField(min_length=4, max_length=4)
    sms_captcha = forms.CharField(min_length=6, max_length=6)

    def clean(self):
        clean_data = super(RegisterForm, self).clean()

        password1 = clean_data.get('password1')
        password2 = clean_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("两次输入的密码不一致！")

        # 前端页面传过来的图形验证码(img_captcha)
        img_captcha = clean_data.get('img_captcha')
        # 从缓存中取出图形验证码(img_captcha)
        cached_img_captcha = cache.get(img_captcha.lower())
        if not cached_img_captcha or img_captcha.lower() != cached_img_captcha.lower():
            raise forms.ValidationError("图形验证码错误！")

        # 因为缓存短信验证是以telephone作为key,短信验证码为value存储
        telephone = clean_data.get('telephone')
        # 从前端获取短信验证码
        sms_captcha = clean_data.get('sms_captcha')
        cached_sms_captcha = cache.get(telephone)
        if not cached_sms_captcha or sms_captcha.lower() != cached_sms_captcha.lower():
            raise forms.ValidationError("短信验证码错误！")

        # 手机号码是否应被注册
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError("手机号已经被注册！")
