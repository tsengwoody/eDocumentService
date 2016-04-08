# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('genericUser', '0002_auto_20160406_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 4, 6, 12, 7, 21, 981060, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 4, 6, 12, 7, 21, 982247, tzinfo=utc)),
        ),
    ]
