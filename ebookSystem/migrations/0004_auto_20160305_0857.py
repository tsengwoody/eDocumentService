# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0003_auto_20160229_0839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ebook',
            name='scan_date',
        ),
        migrations.AddField(
            model_name='book',
            name='get_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='upload_date',
            field=models.DateField(default=datetime.date(2016, 3, 5)),
        ),
        migrations.AddField(
            model_name='ebook',
            name='deadline',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ebook',
            name='get_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='education',
            field=models.CharField(max_length=30, choices=[('\u9ad8\u4e2d', '\u9ad8\u4e2d'), ('\u5b78\u58eb', '\u5b78\u58eb'), ('\u78a9\u58eb', '\u78a9\u58eb')]),
        ),
    ]
