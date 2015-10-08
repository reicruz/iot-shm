# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0010_sensorrds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='building',
        ),
        migrations.DeleteModel(
            name='Sensor',
        ),
    ]
