# Generated by Django 3.2 on 2021-05-05 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0002_alter_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='postcode',
            field=models.IntegerField(),
        ),
    ]
