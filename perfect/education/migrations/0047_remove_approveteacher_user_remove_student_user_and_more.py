# Generated by Django 5.1.6 on 2025-02-08 05:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0046_approveteacher_user_student_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approveteacher',
            name='user',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.AddField(
            model_name='study_material',
            name='class_obj',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='sm', to='education.class'),
        ),
    ]
