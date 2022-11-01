# Generated by Django 4.0.3 on 2022-09-10 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registerDataProvider', '0005_alter_registerdataprovider_approval_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registerdataprovider',
            name='approval_document',
        ),
        migrations.AddField(
            model_name='registerdataprovider',
            name='authorisation_letter',
            field=models.FileField(default='default.pdf', upload_to='authorisation_letters'),
        ),
    ]
