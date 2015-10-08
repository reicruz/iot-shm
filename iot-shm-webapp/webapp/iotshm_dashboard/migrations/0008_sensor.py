# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0007_auto_20150125_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('building', models.ForeignKey(to='iotshm_dashboard.Building')),
            ],
            options={
                'managed': True,
                'db_table': 'Sensor',
            },
            bases=(models.Model,),
        ),
    ]
