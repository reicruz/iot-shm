# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0008_sensor'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('x_health', models.IntegerField()),
                ('y_health', models.IntegerField()),
                ('z_health', models.IntegerField()),
            ],
            options={
                'db_table': 'Health',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Magnitude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('x_magnitude', models.FloatField()),
                ('y_magnitude', models.FloatField()),
                ('z_magnitude', models.FloatField()),
                ('frequency', models.FloatField()),
            ],
            options={
                'db_table': 'Magnitude',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
