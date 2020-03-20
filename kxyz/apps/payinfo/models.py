from django.db import models
from shortuuidfield import ShortUUIDField


class Payinfo(models.Model):
    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=200)
    price = models.FloatField()
    # 文档在我们项目中的处在的位置,文件存储的路径
    path = models.FilePathField()


class PayinfoOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    payinfo = models.ForeignKey('Payinfo', on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey('kxyzauth.User', on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 选择支付的方式,1是支付宝 2是微信 3是比特币
    istype = models.SmallIntegerField(default=0)
    # 用户是否已经购买, 默认为1(未购买),购买之后更新数据库,该字段值变成2
    status = models.SmallIntegerField(default=1)
