# Generated by Django 4.0.3 on 2022-04-05 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EVUpdates', '0009_remove_evlocations_cost_per_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='evlocations',
            name='dtl_site',
            field=models.BooleanField(default=True),
        ),
    ]