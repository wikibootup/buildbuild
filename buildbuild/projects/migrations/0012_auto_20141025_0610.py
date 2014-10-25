# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20141025_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='docker_text',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='project',
            name='properties',
            field=jsonfield.fields.JSONField(default=(b'', b'')),
        ),
    ]
