# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-08 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20190307_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.CharField(max_length=10)),
                ('productimg', models.CharField(max_length=200)),
                ('productname', models.CharField(max_length=100)),
                ('productlongname', models.CharField(max_length=200)),
                ('isxf', models.BooleanField(default=False)),
                ('pmdesc', models.BooleanField(default=False)),
                ('specifics', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('marketprice', models.FloatField()),
                ('categoryid', models.CharField(max_length=10)),
                ('childcid', models.CharField(max_length=10)),
                ('childcidname', models.CharField(max_length=50)),
                ('dealerid', models.CharField(max_length=10)),
                ('storenums', models.IntegerField()),
                ('productnum', models.IntegerField()),
            ],
            options={
                'db_table': 'axf_goods',
            },
        ),
    ]
