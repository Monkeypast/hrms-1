# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_empreview_review_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpPossibleResigneeReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('satisfaction', models.DecimalField(decimal_places=2, max_digits=3)),
                ('evaluation', models.DecimalField(decimal_places=2, max_digits=3)),
                ('projectCount', models.IntegerField()),
                ('averageMonthlyHours', models.IntegerField()),
                ('yearsAtCompany', models.IntegerField()),
                ('workAccident', models.IntegerField(choices=[(0, 'NO'), (1, 'YES')])),
                ('promotion', models.IntegerField(choices=[(0, 'NO'), (1, 'YES')])),
                ('department', models.IntegerField(choices=[(0, 'sales'), (1, 'accounting'), (2, 'hr'), (3, 'technical'), (4, 'support'), (5, 'management'), (6, 'IT'), (7, 'product_mng'), (8, 'marketing'), (9, 'RandD')])),
                ('salary', models.IntegerField(choices=[(0, 'LOW'), (1, 'MEDIUM'), (2, 'HIGH')])),
                ('turnover', models.IntegerField(choices=[(0, 'NO'), (1, 'YES')])),
            ],
        ),
    ]
