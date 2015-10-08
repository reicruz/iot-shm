# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0011_auto_20150301_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthRDS',
            fields=[
                ('sensor_id', models.CharField(serialize=False, primary_key=True, max_length=300)),
                ('timestamp', models.DateTimeField(primary_key=True)),
                ('reading_type', models.IntegerField()),
                ('healthy', models.IntegerField()),
            ],
            options={
                'db_table': 'Health',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MagnitudeRDS',
            fields=[
                ('sensor_id', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField()),
                ('value', models.FloatField()),
                ('reading_type', models.IntegerField()),
                ('frequency', models.FloatField()),
                ('reading_id', models.CharField(serialize=False, primary_key=True, max_length=300)),
            ],
            options={
                'db_table': 'Magnitude',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
