# Generated by Django 3.1.2 on 2021-01-09 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20210109_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='uuid',
            field=models.UUIDField(default=None),
            preserve_default=False,
        ),
    ]