"""
    用于判断payinfo.html页面中用户是否已经购买,只返回True/False
"""

# 导入过滤器模板
from django import template
from apps.payinfo.models import PayinfoOrder

# 在过滤器中注册下
register = template.Library()


@register.filter
def is_buyed(payinfo, user):
    if user.is_authenticated:
        result = PayinfoOrder.objects.filter(payinfo=payinfo, buyer=user, status=2).exists()
        return result
    else:
        return False
