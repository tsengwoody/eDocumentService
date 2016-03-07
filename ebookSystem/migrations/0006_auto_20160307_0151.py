# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ebookSystem', '0005_auto_20160306_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_datetime', models.DateField(default=datetime.datetime(2016, 3, 7, 1, 51, 12, 779448, tzinfo=utc))),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.RemoveField(
            model_name='contactus',
            name='message_date',
        ),
        migrations.AddField(
            model_name='contactus',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 3, 7, 1, 51, 12, 778733, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='book',
            name='upload_date',
            field=models.DateField(default=datetime.date(2016, 3, 7)),
        ),
        migrations.AddField(
            model_name='reply',
            name='contact_us',
            field=models.ForeignKey(to='ebookSystem.ContactUs'),
        ),
    ]
