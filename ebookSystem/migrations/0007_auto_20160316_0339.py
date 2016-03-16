# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0006_auto_20160307_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2016, 3, 16, 3, 39, 33, 388136, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 3, 16, 3, 39, 33, 390556, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ebook',
            name='get_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 3, 16, 3, 39, 33, 391282, tzinfo=utc)),
        ),
    ]
