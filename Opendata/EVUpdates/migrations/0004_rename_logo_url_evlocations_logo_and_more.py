# Generated by Django 4.0.3 on 2022-04-02 08:30

import EVUpdates.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EVUpdates', '0003_evlocations_provider_passcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evlocations',
            old_name='logo_url',
            new_name='logo',
        ),
        migrations.RenameField(
            model_name='evlocations',
            old_name='vendor_name',
            new_name='vendor',
        ),
        migrations.RemoveField(
            model_name='evlocations',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='evlocations',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='evlocations',
            name='uid',
        ),
        migrations.AddField(
            model_name='evlocations',
            name='coordinates',
            field=models.JSONField(blank=True, null=True, validators=[EVUpdates.models.EVLocations.coordinates_validator]),
        ),
        migrations.AddField(
            model_name='evlocations',
            name='postal_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='evlocations',
            name='charger_type',
            field=models.JSONField(blank=True, null=True, validators=[EVUpdates.models.EVLocations.charger_type_validator]),
        ),
        migrations.AlterField(
            model_name='evlocations',
            name='id',
            field=models.CharField(blank=True, max_length=100, primary_key=True, serialize=False),
        ),
    ]