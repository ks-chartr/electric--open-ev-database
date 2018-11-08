# Generated by Django 2.1.2 on 2018-11-08 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactusform', '0007_auto_20181030_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactrequest',
            name='phone',
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='name',
            field=models.CharField(default='Unkown', max_length=100),
        ),
        migrations.AlterField(
            model_name='downloaddata',
            name='purpose',
            field=models.CharField(default='', max_length=300, null=True),
        ),
    ]