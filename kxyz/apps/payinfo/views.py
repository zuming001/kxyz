from django.shortcuts import render
from .models import Payinfo, PayinfoOrder
from apps.kxyzauth.decorators import kxyz_login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from utils import restful
from django.http import FileResponse
from django.conf import settings
import os


def index(request):
    context = {
        'payinfos': Payinfo.objects.all()
    }
    return render(request, 'payinfo/payinfo.html', context=context)


@kxyz_login_required
def payinfo_order(request):
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = Payinfo.objects.get(pk=payinfo_id)
    order = PayinfoOrder.objects.create(payinfo=payinfo, buyer=request.user, status=1, amount=payinfo.price)
    context = {
        'goods': {
            'thumbnail': payinfo.path,
            'price': payinfo.price,
            'title': payinfo.title
        },
        'order': order,
        'notify_url': request.build_absolute_uri(reverse('payinfo:notify_view')),
        'return_url': request.build_absolute_uri(reverse('payinfo:index'))
    }
    return render(request, 'course/course_order.html', context=context)


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    PayinfoOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()


@kxyz_login_required
def download(request):
    payinfo_id = request.GET.get('payinfo_id')
    order = PayinfoOrder.objects.filter(payinfo_id=payinfo_id, buyer=request.user, status=2)[0]
    if order:
        payinfo = order.payinfo
        path = payinfo.path
        # path = /a/b/c.pdf 或者 /a/xx.jpg
        fp = open(os.path.join(settings.MEDIA_ROOT, path), 'rb')
        response = FileResponse(fp)
        # 下载文件的格式是图片 和 pdf文档的形式
        response['Content-Type'] = 'image/jpeg'
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment;filename="%s"' % path.split("/")[-1]
        return response
    else:
        return render(request, '404.html')
