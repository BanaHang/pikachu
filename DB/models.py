from django.db import models

# Create your models here.


# 项目表，属性分别为序号（PID）、名称（NAME）、日期（DATE）
class Projects(models.Model):
    PID = models.IntegerField(blank=False, primary_key=True)
    NAME = models.CharField(max_length=100, blank=False)
    DATE = models.CharField(max_length=100, blank=True)


# 访问度表，PID外键，所属的项目、访问次数（HOT）
class Hot(models.Model):
    PID = models.IntegerField(blank=False)
    HOT = models.IntegerField(blank=False, default=0)


# 项目页评论表，FID为评论序号、PID为从属项目的序号、TIME为评论时间、CONTENT为评论内容、WRITER为作者
class Follows(models.Model):
    FID = models.AutoField(primary_key=True, blank=False)
    PID = models.IntegerField(blank=False)
    TIME = models.CharField(blank=True, max_length=100)
    CONTENT = models.CharField(blank=True, max_length=550)
    WRITER = models.CharField(blank=True, max_length=100)


# 贴子表，PID为帖子序号、TITLE为帖子标题、CONTENT为帖子内容、TIME为发帖时间、WRITER为帖子作者
class Plate(models.Model):
    PID = models.AutoField(primary_key=True, blank=False)
    TITLE = models.CharField(max_length=100, blank=False)
    CONTENT = models.CharField(max_length=550, blank=True)
    TIME = models.CharField(max_length=100, blank=True)
    WRITER = models.CharField(max_length=100, blank=True)


# 帖子评论表
class Comment(models.Model):
    CID = models.AutoField(primary_key=True, blank=False)
    PID = models.IntegerField(blank=False)
    TIME = models.CharField(max_length=100, blank=True)
    CONTENT = models.CharField(max_length=350, blank=True)
    WRITER = models.CharField(max_length=100, blank=True)
