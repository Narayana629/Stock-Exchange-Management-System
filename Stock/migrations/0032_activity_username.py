# Generated by Django 3.2 on 2021-05-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0031_auto_20210507_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='username',
            field=models.CharField(default='username', max_length=60),
            preserve_default=False,
        ),
    ]
