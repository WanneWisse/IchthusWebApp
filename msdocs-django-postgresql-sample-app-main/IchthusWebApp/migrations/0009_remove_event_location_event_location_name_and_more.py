# Generated by Django 4.1.3 on 2022-12-31 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IchthusWebApp', '0008_event_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
        migrations.AddField(
            model_name='event',
            name='location_name',
            field=models.CharField(default='locatie', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='location_url',
            field=models.CharField(default='locatie', max_length=200),
            preserve_default=False,
        ),
    ]
