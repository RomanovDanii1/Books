# Generated by Django 4.1.4 on 2023-10-18 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0004_bookreadingtime_total_reading_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_reading_7_days', models.FloatField(default=0.0)),
                ('total_reading_30_days', models.FloatField(default=0.0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
