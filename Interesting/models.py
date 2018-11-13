from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Type(models.Model):
    type = models.CharField(max_length=10)

    class Meta:
        db_table = 'type'  # 数据库的表名
        verbose_name_plural = "分类"

    def __str__(self):
        return self.type

class Interesting(models.Model):
    things=models.CharField(max_length=50)
    type=models.ForeignKey(Type,on_delete=models.CASCADE)
    content=RichTextUploadingField()
    create_time=models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'Interest'  # 数据库的表名
        verbose_name_plural = "好玩"
        ordering=['-create_time',]

    def __str__(self):
        return self.things