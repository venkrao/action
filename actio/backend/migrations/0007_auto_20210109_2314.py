# Generated by Django 3.1.2 on 2021-01-09 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20210109_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesubcategory',
            name='catchphrase',
            field=models.CharField(max_length=126),
        ),
    ]
