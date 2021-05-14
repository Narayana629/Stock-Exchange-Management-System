# Generated by Django 3.2 on 2021-05-06 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0025_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('dateofbirth', models.DateField()),
                ('phone', models.IntegerField()),
                ('qualification', models.CharField(max_length=20)),
                ('address1', models.CharField(max_length=60)),
                ('address2', models.CharField(max_length=60)),
                ('state', models.CharField(max_length=25)),
                ('postcode', models.IntegerField()),
                ('city', models.CharField(max_length=25)),
                ('country', models.CharField(max_length=25)),
                ('photo', models.ImageField(default='', upload_to='photos')),
            ],
        ),
    ]
