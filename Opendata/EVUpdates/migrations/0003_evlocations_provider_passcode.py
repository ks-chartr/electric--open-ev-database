# Generated by Django 4.0.3 on 2022-03-19 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EVUpdates', '0002_alter_evlocations_available_alter_evlocations_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='evlocations',
            name='provider_passcode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
