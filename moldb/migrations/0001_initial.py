# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Molecule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('smiles', models.CharField(max_length=500)),
                ('pic', models.ImageField(upload_to='/pics')),
            ],
        ),
    ]
