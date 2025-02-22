from django.db import models
import datetime

class Patient(models.Model):
    PatientID = models.CharField(max_length=50, unique=True)  # Unique ID for each patient
    P_National_ID = models.CharField(max_length=20, unique=True)  # Ensuring unique national ID
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Date_of_Birth = models.DateField()
    Gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    Address = models.TextField()
    Fhir_ID = models.AutoField(primary_key=True, unique=True)
    Phone_Number = models.IntegerField()
    last_arrived = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.First_Name} {self.Last_Name} ({self.P_National_ID})"


class MedicalRecord(models.Model):
    RecordID = models.AutoField(primary_key=True)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Link to Patient
    Diagnosis = models.TextField()
    Treatment = models.TextField()
    Date_Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical Record {self.RecordID} for {self.Patient}"


class Appointment(models.Model):
    AppointmentID = models.AutoField(primary_key=True)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Link to Patient
    Appointment_Date = models.DateTimeField()
    Doctor_Name = models.CharField(max_length=100)
    Notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment {self.AppointmentID} - {self.Patient.First_Name}"
