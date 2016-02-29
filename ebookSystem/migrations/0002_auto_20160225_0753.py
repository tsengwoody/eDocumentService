# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebook',
            name='service_hours',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='editor',
            name='professional_field',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='editor',
            name='service_hours',
            field=models.IntegerField(default=0),
        ),
    ]
