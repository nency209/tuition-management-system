# Generated by Django 5.1.6 on 2025-02-23 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0062_alter_inquiry_area_alter_inquiry_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='area',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='city',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='code',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='state',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='area',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='city',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='code',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='state',
        ),
    ]
