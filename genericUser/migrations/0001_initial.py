# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.contrib.auth.models
from django.utils.timezone import utc
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=30)),
                ('birthday', models.DateField()),
                ('education', models.CharField(max_length=30, choices=[('\u9ad8\u4e2d', '\u9ad8\u4e2d'), ('\u5b78\u58eb', '\u5b78\u58eb'), ('\u78a9\u58eb', '\u78a9\u58eb')])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('message_datetime', models.DateField(default=datetime.datetime(2016, 4, 6, 12, 7, 20, 847597, tzinfo=utc))),
                ('kind', models.CharField(max_length=10, choices=[('\u6821\u5c0d\u554f\u984c', '\u6821\u5c0d\u554f\u984c'), ('\u7cfb\u7d71\u554f\u984c', '\u7cfb\u7d71\u554f\u984c'), ('\u71df\u904b\u5efa\u8b70', '\u71df\u904b\u5efa\u8b70'), ('\u52a0\u5165\u6211\u5011', '\u52a0\u5165\u6211\u5011'), ('\u5176\u4ed6', '\u5176\u4ed6')])),
                ('subject', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_datetime', models.DateField(default=datetime.datetime(2016, 4, 6, 12, 7, 20, 848569, tzinfo=utc))),
                ('content', models.CharField(max_length=1000)),
                ('contact_us', models.ForeignKey(to='genericUser.ContactUs')),
            ],
        ),
    ]
