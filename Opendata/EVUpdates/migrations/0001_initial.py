# Generated by Django 3.2.15 on 2022-11-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectorMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_connector_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mapped_connector_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EVLocations',
            fields=[
                ('id', models.CharField(blank=True, max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('vendor', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('coordinates', models.CharField(blank=True, max_length=100, null=True)),
                ('charger_type', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('open', models.CharField(blank=True, max_length=100, null=True)),
                ('close', models.CharField(blank=True, max_length=100, null=True)),
                ('logo', models.TextField(blank=True, null=True)),
                ('staff', models.CharField(blank=True, max_length=100, null=True)),
                ('total', models.CharField(blank=True, max_length=100, null=True)),
                ('available', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_modes', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_numbers', models.CharField(blank=True, max_length=100, null=True)),
                ('provider_passcode', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('dtl_site', models.BooleanField(default=True)),
                ('station_type', models.CharField(default='charging', max_length=50)),
            ],
        ),
    ]
