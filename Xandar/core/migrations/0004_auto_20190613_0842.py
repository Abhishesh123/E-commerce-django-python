# Generated by Django 2.1.7 on 2019-06-13 08:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190612_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsubcategory',
            name='category',
        ),
        migrations.AlterField(
            model_name='coupons',
            name='valid_till',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 13, 8, 42, 22, 235365)),
        ),
    ]