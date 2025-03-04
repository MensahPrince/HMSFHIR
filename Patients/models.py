from django.db import models
import datetime

class Patient(models.Model):
    PatientID = models.CharField(max_length=100, unique=True)
    P_National_ID = models.CharField(max_length=100)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Date_of_Birth = models.DateField()
    Gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    Address = models.CharField(max_length=255)
    Fhir_ID = models.AutoField(primary_key=True, unique=True)
    Phone_Number = models.CharField(max_length=15)
    last_arrived = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.First_Name} {self.Last_Name} ({self.P_National_ID})"

    def get_medical_records(self):
        return self.medicalrecord_set.all()

class MedicalRecord(models.Model):
    RecordID = models.AutoField(primary_key=True)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Link to Patient
    Diagnosis = models.TextField()
    Treatment = models.TextField()
    Date_Created = models.DateTimeField(auto_now_add=True)
    Clinical_Status = models.CharField(max_length=100, blank=True, null=True)
    Verification_Status = models.CharField(max_length=100, blank=True, null=True)
    Category = models.CharField(max_length=100, blank=True, null=True)
    Severity = models.CharField(max_length=100, blank=True, null=True)
    Code = models.CharField(max_length=100, blank=True, null=True)
    Subject = models.CharField(max_length=100, blank=True, null=True)
    Encounter = models.CharField(max_length=100, blank=True, null=True)
    Onset = models.DateTimeField(blank=True, null=True)
    Abatement = models.DateTimeField(blank=True, null=True)
    Recorded_Date = models.DateTimeField(blank=True, null=True)
    Recorder = models.CharField(max_length=100, blank=True, null=True)
    Asserter = models.CharField(max_length=100, blank=True, null=True)
    Stage = models.CharField(max_length=100, blank=True, null=True)
    Evidence = models.CharField(max_length=100, blank=True, null=True)
    Note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Medical Record {self.RecordID} for {self.Patient}"

class Appointment(models.Model):
    AppointmentID = models.AutoField(primary_key=True)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Appointment_Date = models.DateTimeField()
    Doctor_Name = models.CharField(max_length=100)
    Notes = models.TextField(blank=True, null=True)
    Appointment_Status = models.CharField(max_length=10, choices=[('Completed', 'Completed'), ('Scheduled', 'Scheduled'), ('Cancelled', 'Cancelled')], default='Scheduled')

    def __str__(self):
        return f"Appointment {self.AppointmentID} - {self.Patient.First_Name}"
