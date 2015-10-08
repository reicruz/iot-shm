# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0006_auto_20150124_1028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='building_manager',
            new_name='manager',
        ),
        migrations.RenameField(
            model_name='building',
            old_name='building_number',
            new_name='number',
        ),
        migrations.AddField(
            model_name='building',
            name='name',
            field=models.CharField(default='Parking Deck', max_length=300),
            preserve_default=False,
        ),
    ]
