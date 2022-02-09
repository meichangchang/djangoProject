# Create your models here.

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    # upload_to 指定上传文件位置
    # 这里指定存放在 img/ 目录下
    headimg = models.FileField(upload_to="images/")

    # 返回名称
    def __str__(self):
        return self.name
