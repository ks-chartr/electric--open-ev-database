# Generated by Django 2.1.2 on 2018-10-30 20:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contactusform', '0006_downloaddata_datadownloaded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='downloaddata',
            name='number',
        ),
        migrations.RemoveField(
            model_name='downloaddata',
            name='org',
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='subject',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='downloaddata',
            name='email',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='downloaddata',
            name='usageType',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='downloaddata',
            name='name',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='downloaddata',
            name='purpose',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
