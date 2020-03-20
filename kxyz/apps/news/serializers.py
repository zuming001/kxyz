'''
    使用Django REST framework 将数据库中的数据序列化
'''

from rest_framework import serializers
from .models import News, NewsCategory, Comment, Banner
from apps.kxyzauth.serializers import UserSerializers


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name']  # 指定序列化字段


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializers()

    class Meta:
        model = News
        fields = ['id', 'title', 'desc', 'thumbnail', 'pub_time', 'category', 'author']  # 指定序列化字段


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializers()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'pub_time', 'author']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image_url', 'link_to', 'priority']
