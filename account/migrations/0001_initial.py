# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('genericUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('service_hours', models.IntegerField(default=0)),
                ('professional_field', models.CharField(max_length=30, null=True, blank=True)),
                ('is_book', models.BooleanField(default=False)),
                ('is_editing', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'editor',
            },
        ),
    ]
