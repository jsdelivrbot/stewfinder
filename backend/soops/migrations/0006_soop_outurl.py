# Generated by Django 2.0.4 on 2018-04-30 02:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('soops', '0005_soop_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='soop',
            name='outUrl',
            field=models.CharField(default=django.utils.timezone.now, max_length=500),
            preserve_default=False,
        ),
    ]
