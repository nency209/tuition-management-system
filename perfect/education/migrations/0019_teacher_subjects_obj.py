# Generated by Django 5.1.4 on 2025-02-03 06:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0018_staff_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='Subjects_obj',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='education.subjects'),
        ),
    ]
