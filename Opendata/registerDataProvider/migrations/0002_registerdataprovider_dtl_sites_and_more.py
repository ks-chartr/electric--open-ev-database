# Generated by Django 4.0.3 on 2022-03-30 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registerDataProvider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerdataprovider',
            name='dtl_sites',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registerdataprovider',
            name='nondtl_sites',
            field=models.BooleanField(default=False),
        ),
    ]
