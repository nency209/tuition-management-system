# Generated by Django 5.1.4 on 2025-02-04 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0030_alter_gallery_image_alter_study_material_pdf_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(upload_to='gallery/'),
        ),
        migrations.AlterField(
            model_name='study_material',
            name='pdf_url',
            field=models.FilePathField(),
        ),
    ]
