# Generated by Django 3.2 on 2021-05-06 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0010_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='buystock',
            name='price',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
