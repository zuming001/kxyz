# Generated by Django 2.2.7 on 2019-11-19 08:47

from django.db import migrations, models
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False, verbose_name='uid')),
                ('telephone', models.CharField(max_length=11, unique=True, verbose_name='手机号')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('username', models.CharField(max_length=100, verbose_name='用户名')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用,默认为True')),
                ('is_staff', models.BooleanField(default=False, verbose_name='是否为员工,默认不是')),
                ('date_join', models.DateTimeField(auto_now_add=True, verbose_name='用户何时注册的')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
