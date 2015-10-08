# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0004_auto_20150124_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='zipcode',
            field=models.IntegerField(max_length=5),
            preserve_default=True,
        ),
    ]
