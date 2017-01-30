# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_no_of_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='init_time',
            field=models.CharField(default=b'0', max_length=50),
        ),
    ]
