from django.shortcuts import render
from .models import News, NewsCategory
from django.conf import settings
from utils import restful
from .serializers import NewsSerializer, CommentSerializer
from django.http import Http404
from .forms import PublicCommentForms
from .models import Comment
from apps.kxyzauth.decorators import kxyz_login_required
from .models import Banner


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    # 因为该查询语句不会提前将字段中的外键的值查询出来,所以会产生额外的sql查询
    # newes = News.objects.all()[0:count]
    # select_related('category','author') 会将表中外键'category','author'这两个字段的值一起查出,不会产生额外的sql查询
    newes = News.objects.select_related('category', 'author').all()[0:count]
    # 因为NewCategory中的数据基本上不会发生改变,那么我们可以将表中的数据放在"缓存中",这种可以优化性能
    categories = NewsCategory.objects.all()
    context = {
        'newes': newes,
        'categoryes': categories,
        'banners': Banner.objects.all()
    }
    return render(request, 'news/index.html', context=context)


def news_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    page = int(request.GET.get('p', 1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id', 0))
    # 0,1
    # 2,3
    # 4,5
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        # QuerySet
        # {'id':1, 'title':'abc', 'category':{'id':1,'name':'热点'}}
        newses = News.objects.select_related('category', 'author').all()[start:end]
    else:
        newses = News.objects.select_related('category', 'author').filter(category_id=category_id)[start:end]
    # many 代表很多的数据都要序列化
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.result(data=data)


def news_detail(request, news_id):
    try:
        # 因为get方法,其中参数在数据库中的值是唯一的,否则会报错,所以需要做错误处理
        news = News.objects.select_related('category', 'author').prefetch_related("comments__author").get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    # 如果出现新闻不存在,就报404错误
    except News.DoesNotExist:
        raise Http404


@kxyz_login_required
def public_comment(request):
    form = PublicCommentForms(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        try:
            news = News.objects.get(pk=news_id)
        except:
            return restful.params_error(message='用户不存在')
        comment = Comment.objects.create(content=content, news=news, author=request.user)
        serializer = CommentSerializer(comment)
        return restful.result(data=serializer.data)
    else:
        return restful.params_error(message=form.get_errors())


def search(request):
    return render(request, 'search/search.html')
