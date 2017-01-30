# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='upliner',
        ),
        migrations.AddField(
            model_name='profile',
            name='upliner',
            field=models.ManyToManyField(related_name='upliner', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
