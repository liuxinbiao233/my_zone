# Generated by Django 2.1.1 on 2018-10-26 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_list',
            name='Picture1',
            field=models.ImageField(blank=True, upload_to='category'),
        ),
    ]
