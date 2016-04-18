# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('genericUser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 4, 18, 11, 52, 15, 109351, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 4, 18, 11, 52, 15, 110175, tzinfo=utc)),
        ),
    ]
