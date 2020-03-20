from django.shortcuts import render
from django.urls import reverse
from .models import Course, CourseOrder
from django.conf import settings
import os, time, hashlib, hmac
from utils import restful
from apps.kxyzauth.decorators import kxyz_login_required
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt


def index(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'course/course_index.html', context=context)


def course_detail(request, course_id):
    try:
        course = Course.objects.filter(pk=course_id)[0]
    except ValueError:
        return render(request, '404.html')
    # 用户是否已经购买了该视频
    buyed = CourseOrder.objects.filter(course=course, buyer=request.user, status=2).exists()
    context = {
        'course': course,
        'buyed': buyed
    }
    return render(request, 'course/course_detail.html', context=context)


def course_token(request):
    # 视频的 url
    file = request.GET.get("video")

    course_id = request.GET.get("course_id")

    if not CourseOrder.objects.filter(course_id=course_id, buyer=request.user, status=2).exists():
        return restful.params_error(message='请先购买课程! ')

    # token的过期时间 为两个小时
    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # file = http://jmvi6gv2zgxb65v5f2r.exp.bcevod.com/mda-jmvih7nruwyfr5vv/mda-jmvih7nruwyfr5vv.m3u8
    # os.path.splitext 将url分为['http://jmvi6gv2zgxb65v5f2r.exp.bcevod.com/mda-jmvih7nruwyfr5vv/mda-jmvih7nruwyfr5vv','.m3u8']
    extension = os.path.splitext(file)[1]
    # 最终获得视频的media_id
    media_id = file.split('/')[-1].replace(extension, '')

    # 因为USER_KEY被加密生成signature 所以需要encode
    key = USER_KEY.encode('utf-8')

    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)

    return restful.result(data={'token': token})


@kxyz_login_required
def course_order(request, course_id):
    try:
        course = Course.objects.filter(pk=course_id)[0]
    except ValueError:
        return restful.params_error(message='没有该课程')

    order = CourseOrder.objects.filter(course=course, buyer=request.user, amount=course.price, status=2)

    # 如果客户已经购买过视频,就直接渲染课程详情页
    if order:
        return reverse('course:course_detail', kwargs={'course_id': course.pk})
    else:
        order = CourseOrder.objects.create(course=course, buyer=request.user, amount=course.price)
        context = {
            'goods': {
                'thumbnail': course.cover_url,
                'title': course.title,
                'price': course.price
            },
            'order': order,
            # 将域名+ 端口号 + /course/notify_view/ 修改CourseOrder中status=2,标记用户已经付款
            'notify_url': request.build_absolute_uri(reverse('course:notify_view')),
            # 付款执行完成需要跳转的页面,直接跳转到视频的页面
            'return_url': request.build_absolute_uri(reverse('course:course_detail', kwargs={'course_id': course.pk}))
        }
        return render(request, 'course/course_order.html', context=context)


@kxyz_login_required
def course_order_key(request):
    price = request.POST.get("price")
    notify_url = request.POST.get("notify_url")
    return_url = request.POST.get("return_url")
    orderid = request.POST.get("orderid")
    istype = request.POST.get("istype")
    goodsname = request.POST.get("goodsname")

    token = '5344eb1ee2799752ec386d07600eccaa'
    uid = '270aa06fa41ff7ff60295f9a'
    orderuid = str(request.user.pk)

    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        'utf-8')).hexdigest()

    return restful.result(data={'key': key})


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get("orderid")
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()
