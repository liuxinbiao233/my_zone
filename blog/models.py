from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNUm_ExpandMethod,ReadDetail

# Create your models here.


class Blog_Type(models.Model):
    type_name=models.CharField(max_length=10)

    class Meta:
        db_table='blog_type' #数据库的表名
        verbose_name_plural="博客分类"
    def __str__(self):
        return self.type_name

class Blog(models.Model,ReadNUm_ExpandMethod):
    title=models.CharField(max_length=50)
    blog_type=models.ForeignKey(Blog_Type,on_delete=models.CASCADE)
    content=RichTextUploadingField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    read_details=GenericRelation(ReadDetail)
    create_time=models.DateTimeField(auto_now_add=True)
    last_charge_time=models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'Blog'  # 数据库的表名
        verbose_name_plural = "博客列表"
        ordering=['-create_time',]


    def __str__(self):
        return self.title

    def length(self):
        if len(str(self.content))>>10:
            return '{}......'.format(str(self.content)[0:10])
        else:
            return str(self.content)
    length.allow_tags=True

