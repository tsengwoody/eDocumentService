# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0009_auto_20160317_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2016, 3, 17, 5, 42, 40, 694124, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 3, 17, 5, 42, 40, 696394, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 3, 17, 5, 42, 40, 697121, tzinfo=utc)),
        ),
    ]
