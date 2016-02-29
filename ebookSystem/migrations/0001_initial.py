# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
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
                ('education', models.CharField(max_length=30)),
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
                ('remark', models.CharField(max_length=255, null=True, blank=True)),
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
                ('scan_date', models.DateField(default=datetime.date(2016, 2, 25))),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('finish_date', models.DateField(null=True, blank=True)),
                ('remark', models.CharField(max_length=255, null=True, blank=True)),
                ('book', models.ForeignKey(to='ebookSystem.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('service_hours', models.IntegerField(null=True, blank=True)),
                ('professional_field', models.CharField(max_length=30)),
                ('is_book', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='ebook',
            name='editor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ebookSystem.Editor', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='ebook',
            unique_together=set([('book', 'part')]),
        ),
    ]
