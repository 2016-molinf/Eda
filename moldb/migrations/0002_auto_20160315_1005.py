# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-15 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moldb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='molecule',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='molecule',
            name='summary_formula',
            field=models.CharField(default='', max_length=99),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='molecule',
            name='name',
            field=models.CharField(max_length=99),
        ),
    ]