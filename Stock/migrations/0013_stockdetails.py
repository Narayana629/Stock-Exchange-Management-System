# Generated by Django 3.2 on 2021-05-06 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0012_alter_buystock_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stockdetails',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=60)),
                ('ticker', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('datebought', models.DateField()),
                ('price', models.FloatField()),
                ('lastprice', models.FloatField()),
            ],
        ),
    ]
