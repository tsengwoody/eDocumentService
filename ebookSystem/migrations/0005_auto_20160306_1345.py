# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0004_auto_20160305_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('message_date', models.DateField()),
                ('kind', models.CharField(max_length=10, choices=[('\u6821\u5c0d\u554f\u984c', '\u6821\u5c0d\u554f\u984c'), ('\u7cfb\u7d71\u554f\u984c', '\u7cfb\u7d71\u554f\u984c'), ('\u71df\u904b\u5efa\u8b70', '\u71df\u904b\u5efa\u8b70'), ('\u52a0\u5165\u6211\u5011', '\u52a0\u5165\u6211\u5011'), ('\u5176\u4ed6', '\u5176\u4ed6')])),
                ('subject', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='upload_date',
            field=models.DateField(default=datetime.date(2016, 3, 6)),
        ),
    ]
