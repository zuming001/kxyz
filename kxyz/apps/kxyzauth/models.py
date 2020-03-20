from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models


class UserManager(BaseUserManager):
    # _create_user用来创建用户
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError('请传入手机号码！')
        if not username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码！')

        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    # create_user用来创建普通用户
    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone=telephone, username=username, password=password, **kwargs)

    # create_superuser用来创建超级用户
    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone=telephone, username=username, password=password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 不使用默认自增长的主键(id)
    # 防止公司用户数量遭到泄露
    # 切结如果自定义User模型,那么必须在第一次运行migrate命令之前就显出案件好User模型
    # uuid/shortuuid
    # Shortuuidfield: pip3 install django-shortuuidfield
    uid = ShortUUIDField(primary_key=True, verbose_name="uid")
    telephone = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email = models.EmailField(unique=True, null=True,verbose_name="邮箱,可以为空字符串")
    username = models.CharField(max_length=100, verbose_name="用户名")
    is_active = models.BooleanField(default=True, verbose_name="是否可用,默认为True")
    is_staff = models.BooleanField(default=False, verbose_name="是否为员工,默认不是")
    date_join = models.DateTimeField(auto_now_add=True, verbose_name="用户何时注册的时间")

    # 后端验证用户登录的,账号就是telephone
    USERNAME_FIELD = 'telephone'
    # 创建超级用户时需要填写的字段值,必填的是电话号码和密码,username是通过REQUIRED_FIELDS = ['username']追加的
    REQUIRED_FIELDS = ['username']
    # 给指定的用户发送邮件
    EMAIL_FILED = "email"

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
