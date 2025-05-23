# Generated by Django 5.1.3 on 2025-02-22 06:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patients', '0002_patient_last_arrived'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='Status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
    ]
