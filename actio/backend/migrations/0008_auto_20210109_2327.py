# Generated by Django 3.1.2 on 2021-01-09 22:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0007_auto_20210109_2314'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coursesubcategory',
            unique_together={('subcategory', 'offered_in_languages')},
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together={('uuid', 'coach', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='sessionpackageoffering',
            unique_together={('course_category', 'course_subcategory', 'session_size')},
        ),
    ]
