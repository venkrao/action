# Generated by Django 3.1.2 on 2021-01-09 22:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0011_auto_20210109_2348'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='session',
            unique_together={('coach', 'user', 'course_category', 'course_subcategory')},
        ),
        migrations.RemoveField(
            model_name='session',
            name='uuid',
        ),
    ]