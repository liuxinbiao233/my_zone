from django.db import models

# Create your models here.

class Category_of_goods(models.Model):

    Name = models.CharField(max_length=100, unique=True)
    Describe = models.TextField(blank=True)
    Picture = models.ImageField(upload_to='category', blank=True)

    class Meta:
        db_table='Category_of_goods' #数据库的表名
        verbose_name_plural="产品分类"
    def __str__(self):
        return self.Name


class Product_List(models.Model):
    Name = models.CharField(max_length=200, unique=True)
    Describe = models.TextField(blank=True)
    Picture = models.ImageField(upload_to='category', blank=True)
    Picture1 = models.ImageField(upload_to='category', blank=True)
    Category=models.ForeignKey(Category_of_goods, on_delete=models.CASCADE)
    vlaue=models.DecimalField(decimal_places=4,max_digits=10)
    Already_to_shelves=models.BooleanField(default=True)
    create_time=models.DateTimeField(auto_now_add=True)
    change_time=models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'Product_List'  # 数据库的表名
        verbose_name_plural = "产品列表"
        ordering=['-create_time',]

    def __str__(self):
        return self.Name