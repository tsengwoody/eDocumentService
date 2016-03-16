# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0007_auto_20160316_0339'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='finish_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ebookSystem.Guest', null=True),
        ),
        migrations.AddField(
            model_name='ebook',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ebook',
            name='is_exchange',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='editor',
            name='is_editing',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2016, 3, 16, 8, 45, 19, 695969, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 3, 16, 8, 45, 19, 698433, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 3, 16, 8, 45, 19, 699170, tzinfo=utc)),
        ),
    ]
