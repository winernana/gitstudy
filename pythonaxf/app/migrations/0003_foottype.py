# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-07 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_mainshow_shop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foottype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeid', models.CharField(max_length=20)),
                ('typename', models.CharField(max_length=100)),
                ('childtypenames', models.CharField(max_length=255)),
                ('typesort', models.IntegerField()),
            ],
            options={
                'db_table': 'axf_foottype',
            },
        ),
    ]
