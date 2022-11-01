# Generated by Django 2.1.2 on 2022-03-14 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloadRealDataForm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterDataProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True, unique=True)),
                ('number', models.CharField(max_length=100, null=True, unique=True)),
                ('companyName', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('passCode', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('authorised', models.BooleanField(default=False)),
                ('hitsToday', models.IntegerField(default=0)),
                ('hitsAllTime', models.IntegerField(default=0)),
                ('lastHit', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
