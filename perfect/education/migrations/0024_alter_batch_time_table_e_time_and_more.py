# Generated by Django 5.1.4 on 2025-02-04 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0023_alter_batch_time_table_e_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch_time_table',
            name='e_time',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='batch_time_table',
            name='time',
            field=models.IntegerField(default=''),
        ),
    ]
