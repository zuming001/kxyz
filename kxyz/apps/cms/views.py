from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.views.decorators.http import require_POST, require_GET
from apps.news.models import NewsCategory, News, Banner
from utils import restful
from .forms import EditNewsCategoryForm, WriteNewsForm, AddBannerForm, EditBannerForm, EditNewsForm, AddNewsCategoryForm
import os
from django.conf import settings
import qiniu
from apps.news.serializers import BannerSerializer
from django.core.paginator import Paginator
from datetime import datetime
# make_aware 将幼稚的时间标记成清醒的时间
from django.utils.timezone import make_aware
from urllib import parse


# CMS首页
@staff_member_required(login_url='index')
def index(request):
    return render(request, 'cms/index.html')


# 新闻列表管理
class NewsListView(View):
    def get(self, request):
        # request.GET 获取出来的所有数据，都是字符串类型
        # 获取页面号,'p'前后端定义页面的变量,如果前端没传,则默认为1
        page = int(request.GET.get('p', 1))
        # 开始日期
        start = request.GET.get("start")
        # 结束日期
        end = request.GET.get("end")
        # 标题
        title = request.GET.get("title")
        # 某种分类的新闻,如果前段没有传某个分类的id,就表示所有的分类
        # request.GET.get(参数,默认值）默认值是指没有参数传递进来时才会使用，如果传递一个空的字符串，默认值不起作用
        category_id = int(request.GET.get("category", 0) or 0)
        # 所有的分类的新闻
        categories = NewsCategory.objects.all()
        newses = News.objects.select_related('category', 'author')

        # 根据新闻发布日期查询
        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2018, month=11, day=28)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            # 根据给定的日期筛选出在时间范围内的新闻
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        # 根据标题查询
        if title:
            # title__icontains 大小写不敏感
            newses = newses.filter(title__icontains=title)

        # 根据分类查询
        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 2)
        page_obj = paginator.page(page)
        context_data = self.get_pagination_data(paginator, page_obj)
        context = {
            'categories': categories,
            # 当前页面的数据
            'newses': page_obj.object_list,
            'paginator': paginator,
            'page_obj': page_obj,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({
                # 如果前端没有传start就将start赋值给一个空字符串，end,title,category也是一样
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or '',
            })
        }
        context.update(context_data)
        return render(request, 'cms/news_list.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages代表当前页面的左边页面的页码
            'left_pages': left_pages,
            # right_pages代表当前页面的右边页面的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


# 编辑新闻列表管理
class EditNewsView(View):
    def get(self, request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context = {
            'news': news,
            'categories': NewsCategory.objects.all()
        }
        return render(request, 'cms/news_release.html', context=context)

    def post(self, request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            desc = form.cleaned_data.get("desc")
            thumbnail = form.cleaned_data.get("thumbnail")
            content = form.cleaned_data.get("content")
            category_id = form.cleaned_data.get("category")
            pk = form.cleaned_data.get("pk")
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.filter(pk=pk).update(title=title, desc=desc, thumbnail=thumbnail, content=content,
                                              category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


# 删除新闻
@require_POST
def delete_news(request):
    news_id = int(request.POST.get("news_id"))
    News.objects.filter(pk=news_id).delete()
    return restful.ok()


# 发布新闻
@staff_member_required(login_url='index')
def news_release(request):
    if request.method == "GET":
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/news_release.html', context=context)
    elif request.method == "POST":
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            desc = form.cleaned_data.get("desc")
            thumbnail = form.cleaned_data.get("thumbnail")
            content = form.cleaned_data.get("content")
            category_id = form.cleaned_data.get("category")
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail, content=content, category=category,
                                author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


# 新闻分类
@require_GET
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/news_category.html', context=context)


# 新增一种新的新闻类别
@require_POST
def add_news_category(request):
    form = AddNewsCategoryForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data.get("name")
        exists = NewsCategory.objects.filter(name=name).exists()
        if not exists:
            NewsCategory.objects.create(name=name)
            return restful.ok()
        else:
            return restful.params_error(message='该分类已经存在! ')
    else:
        return restful.params_error(message=form.get_errors())


# 编辑新闻类别
@require_POST
def edit_news_category(request):
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get("pk")
        name = form.cleaned_data.get("name")
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message="该新闻分类不存在！")
    else:
        return restful.params_error(message=form.get_errors())


# 删除新闻类别
@require_POST
def delete_news_category(request):
    pk = request.POST.get("pk")
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message="该分类不存在!")


# 轮播图管理页面
def banner(request):
    return render(request, 'cms/banners.html')


# 展示轮播图
def banner_list(request):
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return restful.result(data=serializer.data)


# 删除轮播图
def delete_banner(request):
    banner_id = request.POST.get("banner_id")
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()


# 修改轮播图
def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get("pk")
        image_url = form.cleaned_data.get("image_url")
        link_to = form.cleaned_data.get("link_to")
        priority = form.cleaned_data.get("priority")
        Banner.objects.filter(pk=pk).update(image_url=image_url, link_to=link_to, priority=priority)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


# 增加轮播图
def add_banner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get("priority")
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority, image_url=image_url, link_to=link_to)
        return restful.result(data={'banner_id': banner.pk})
    else:
        return restful.params_error(message=form.get_errors())


# 文件上传到本地的media文件夹中
@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    # http://127.0.0.1:8000/media/abc.jpg
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.result(data={'url': url})


# 文件上传到七牛云中
@require_GET
def qntoken(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SERCRET_KEY

    # 存储空间的名称
    bucket = settings.QINIU_BUCKET_NAME
    # 创建授权的信息
    q = qiniu.Auth(access_key, secret_key)

    # 返回给前端js
    token = q.upload_token(bucket)

    return restful.result(data={'token': token})
