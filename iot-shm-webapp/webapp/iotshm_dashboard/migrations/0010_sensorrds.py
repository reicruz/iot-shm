# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0009_healthscore_magnitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorRDS',
            fields=[
                ('building_id', models.IntegerField(serialize=False, primary_key=True)),
                ('id', models.IntegerField(primary_key=True)),
            ],
            options={
                'db_table': 'Sensor',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
