# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=25)),
                ('surname', models.CharField(max_length=25)),
                ('phone', models.CharField(max_length=11)),
                ('bank', models.CharField(max_length=50)),
                ('account_number', models.CharField(max_length=10)),
                ('matched', models.BooleanField(default=False)),
                ('package', models.CharField(default=b'None', max_length=4, choices=[(b'None', b'None'), (b'5k', b'5k'), (b'10k', b'10k'), (b'15k', b'15k'), (b'20k', b'20k'), (b'50k', b'50k'), (b'100k', b'100k'), (b'200k', b'200k'), (b'500k', b'500k')])),
                ('PH_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('PHed', models.BooleanField(default=False)),
                ('deactivated', models.BooleanField(default=False)),
                ('no_of_payers', models.IntegerField(default=0)),
                ('downliner', models.ManyToManyField(related_name='downliner', to=settings.AUTH_USER_MODEL, blank=True)),
                ('upliner', models.OneToOneField(related_name='upliner', blank=True, to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-PH_time',),
            },
        ),
    ]
