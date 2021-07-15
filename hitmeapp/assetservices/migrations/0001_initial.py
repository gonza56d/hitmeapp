# Generated by Django 3.2.5 on 2021-07-15 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoCurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('rank', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('market_cap', models.DecimalField(decimal_places=2, max_digits=9)),
                ('volume', models.DecimalField(decimal_places=2, max_digits=9)),
                ('circulating_supply', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
