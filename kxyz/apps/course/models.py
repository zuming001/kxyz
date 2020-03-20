from django.db import models
from shortuuidfield import ShortUUIDField


class Lecturer(models.Model):
    username = models.CharField(max_length=100)
    # avatar 代表图像
    avatar = models.URLField()
    jobtitle = models.CharField(max_length=100)
    profile = models.TextField()


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)


class Course(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey('CourseCategory', on_delete=models.DO_NOTHING)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.DO_NOTHING)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    # 视频时间长度用秒来表示
    duration = models.IntegerField()
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_time']


class CourseOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    # 购买的课程
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING)
    # 支付者
    buyer = models.ForeignKey('kxyzauth.User', on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1:代表支付宝支付 2.代表微信支付
    istype = models.SmallIntegerField(default=0)
    # 订单支付的状态, 默认为1显示未支付,2代表支付成功
    status = models.SmallIntegerField(default=1)
