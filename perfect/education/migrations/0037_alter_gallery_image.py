# Generated by Django 5.1.4 on 2025-02-05 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0036_alter_gallery_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(upload_to='Pictures\\mom\\'),
        ),
    ]
