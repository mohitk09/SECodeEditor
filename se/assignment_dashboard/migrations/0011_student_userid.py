# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-04 06:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_dashboard', '0010_problem_test_case_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='UserId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='assignment_dashboard.User'),
            preserve_default=False,
        ),
    ]
