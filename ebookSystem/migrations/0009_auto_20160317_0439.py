# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0008_auto_20160316_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='finish_count',
        ),
        migrations.RemoveField(
            model_name='book',
            name='get_count',
        ),
        migrations.RemoveField(
            model_name='ebook',
            name='guest',
        ),
        migrations.RemoveField(
            model_name='ebook',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='book',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2016, 3, 17, 4, 39, 22, 340512, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 3, 17, 4, 39, 22, 342793, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 3, 17, 4, 39, 22, 343514, tzinfo=utc)),
        ),
    ]
