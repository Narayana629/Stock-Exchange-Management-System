# Generated by Django 3.2 on 2021-05-08 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0032_activity_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='', null=True, upload_to='media'),
        ),
    ]
