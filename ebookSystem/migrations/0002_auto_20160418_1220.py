# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ebook',
            name='edit_date',
        ),
        migrations.RemoveField(
            model_name='ebook',
            name='is_edited',
        ),
        migrations.RemoveField(
            model_name='ebook',
            name='is_finish',
        ),
        migrations.AddField(
            model_name='ebook',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='book',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2016, 4, 18, 12, 20, 49, 853845, tzinfo=utc)),
        ),
    ]
