# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '__first__'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookname', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('translator', models.CharField(max_length=50, null=True, blank=True)),
                ('house', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('ISBN', models.CharField(max_length=20)),
                ('path', models.CharField(max_length=255, null=True, blank=True)),
                ('page_count', models.IntegerField(null=True, blank=True)),
                ('part_count', models.IntegerField(null=True, blank=True)),
                ('page_per_part', models.IntegerField(default=50)),
                ('is_active', models.BooleanField(default=False)),
                ('upload_date', models.DateField(default=datetime.datetime(2016, 3, 20, 9, 35, 47, 624874, tzinfo=utc))),
                ('remark', models.CharField(max_length=255, null=True, blank=True)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='guest.Guest', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part', models.IntegerField()),
                ('begin_page', models.IntegerField()),
                ('end_page', models.IntegerField()),
                ('edited_page', models.IntegerField(default=0)),
                ('is_finish', models.BooleanField(default=False)),
                ('is_edited', models.BooleanField(default=False)),
                ('is_exchange', models.BooleanField(default=False)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('finish_date', models.DateField(null=True, blank=True)),
                ('deadline', models.DateField(null=True, blank=True)),
                ('get_date', models.DateField(null=True, blank=True)),
                ('service_hours', models.IntegerField(default=0)),
                ('remark', models.CharField(max_length=255, null=True, blank=True)),
                ('book', models.ForeignKey(to='ebookSystem.Book')),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='account.Editor', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='ebook',
            unique_together=set([('book', 'part')]),
        ),
    ]
