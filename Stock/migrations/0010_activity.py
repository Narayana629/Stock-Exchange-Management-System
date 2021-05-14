# Generated by Django 3.2 on 2021-05-05 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0009_auto_20210505_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('quantity', models.IntegerField()),
                ('datebought', models.DateField()),
            ],
        ),
    ]
