# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0002_auto_20160418_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2016, 4, 18, 12, 23, 58, 928678, tzinfo=utc)),
        ),
    ]
