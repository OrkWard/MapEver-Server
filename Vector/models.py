from django.db import models


class JSONFile(models.Model):
    # 文件名，用作keyword（唯一值）
    name = models.CharField(max_length=100)
    # 数据内容
    data = models.TextField()
