# Generated by Django 5.1.7 on 2025-03-27 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patients', '0009_remove_patient_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='Emergency_Contact_Name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='Emergency_Contact_Phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='Emergency_Contact_Relationship',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='Insurance_Details',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='Marital_Status',
            field=models.CharField(blank=True, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='Middle_Name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
    ]
