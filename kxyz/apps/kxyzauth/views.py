from django.contrib.auth import logout, login, authenticate, get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, reverse
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from utils import restful
from utils.captcha.xfzcaptcha import Captcha
from utils.aliyunsdk import aliyunsms
from django.core.cache import cache
# BytesIO就相当于内存管道一样，将图片存储，生成一个流对象
from io import BytesIO

User = get_user_model()


# API接口的设计
# {"code":400,"message":"","data":{}}

@require_POST
def login_view(request):
    # LoginForm(request.POST) 一定要传入参数
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        # 用于登录验证
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    # 设置为None,则表示使用全局的过期时间(15天)
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:

                return restful.unauth(message="您的账号已经被冻结")
        else:
            return restful.params_error(message="手机号或密码错误")
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        user.save()
        login(request, user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


def img_captcha(request):
    text, image = Captcha.gene_code()
    # image必须借助流，需要用到BytesIO对象,BytesIO相当于一个管道,用来存储图片的理数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()
    #  12Df: 12Df.lower()
    cache.set(text.lower(), text.lower(), 5 * 60)

    return response


def sms_captcha(request):
    # /sms_captcha/?telephone=xxx
    telephone = request.GET.get('telephone')
    code = Captcha.gene_number()
    cache.set(telephone, code, 5 * 60)
    print('短信验证码：',code)
    # result = aliyunsms.send_sms(telephone, code)
    return restful.ok()


def cache_test(request):
    cache.set('username', '小名同学', 60)
    result = cache.get('username')
    print(result)
    return HttpResponse('success')
