# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0003_auto_20150124_0937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='number',
            new_name='building_number',
        ),
        migrations.AddField(
            model_name='building',
            name='address',
            field=models.CharField(max_length=300, default='Peters Parking Deck'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='building',
            name='city',
            field=models.CharField(max_length=100, default='Atlanta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='building',
            name='state',
            field=models.CharField(max_length=2, default='GA'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='building',
            name='zipcode',
            field=models.CharField(max_length=5, default='30313'),
            preserve_default=False,
        ),
    ]
