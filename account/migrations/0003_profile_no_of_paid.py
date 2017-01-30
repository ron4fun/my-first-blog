# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170129_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='no_of_paid',
            field=models.IntegerField(default=0),
        ),
    ]
