# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0002_auto_20160225_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebook',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ebookSystem.Guest', null=True),
        ),
        migrations.AlterField(
            model_name='ebook',
            name='scan_date',
            field=models.DateField(default=datetime.date(2016, 2, 29)),
        ),
    ]
