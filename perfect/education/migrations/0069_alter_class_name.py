# Generated by Django 5.1.6 on 2025-03-23 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0068_alter_teacher_class_obj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
