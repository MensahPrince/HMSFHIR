from django.db import models
import datetime

class Patient(models.Model):
    PatientID = models.CharField(max_length=100, unique=True)
    P_National_ID = models.CharField(max_length=100)
    First_Name = models.CharField(max_length=100)
    Middle_Name = models.CharField(max_length=100, blank=True, null=True)  # Optional middle name
    Last_Name = models.CharField(max_length=100)
    Date_of_Birth = models.DateField()
    Gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    Marital_Status = models.CharField(max_length=20, choices=[
        ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')
    ], blank=True, null=True)
    Address = models.CharField(max_length=255)
    Phone_Number = models.CharField(max_length=15)
    Emergency_Contact_Name = models.CharField(max_length=100, blank=True, null=True)
    Emergency_Contact_Relationship = models.CharField(max_length=50, blank=True, null=True)
    Emergency_Contact_Phone = models.CharField(max_length=15, blank=True, null=True)
    Insurance_Details = models.CharField(max_length=255, blank=True, null=True)
    Fhir_ID = models.AutoField(primary_key=True, unique=True)
    last_arrived = models.DateField(default=datetime.date.today)
    Identifier_Type = models.CharField(
        max_length=50,
        choices=[('national', 'National ID'), ('hospital', 'Hospital ID'), ('insurance', 'Insurance ID')],
        default='hospital'
    )
    def __str__(self):
        return f"{self.First_Name} {self.Last_Name} ({self.P_National_ID})"

    def get_medical_records(self):
        return self.medicalrecord_set.all()



class MedicalRecord(models.Model):
    RecordID = models.AutoField(primary_key=True)
    Patient = models.ForeignKey('Patient', on_delete=models.CASCADE)  # Link to Patient
    Diagnosis = models.TextField()
    Treatment = models.TextField()
    Date_Created = models.DateTimeField(auto_now_add=True)

    Clinical_Status = models.CharField(max_length=100, blank=True, null=True)
    Verification_Status = models.CharField(max_length=100, blank=True, null=True)
    Category = models.CharField(max_length=100, blank=True, null=True)
    Severity = models.CharField(max_length=100, blank=True, null=True)
    Code = models.CharField(max_length=100, blank=True, null=True)

    Subject = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name="medical_records")  # FHIR: Links to Patient
    Encounter = models.ForeignKey('Encounter', on_delete=models.SET_NULL, blank=True, null=True)  # FHIR: Links to Encounter
    Onset = models.CharField(max_length=255, blank=True, null=True)  # Supports Date or Text-based onset
    Abatement = models.CharField(max_length=255, blank=True, null=True)  # Flexible Abatement information

    Recorded_Date = models.DateTimeField(blank=True, null=True)
    Recorder = models.ForeignKey('Practitioner', on_delete=models.SET_NULL, blank=True, null=True)  # FHIR: Links to Practitioner
    Asserter = models.CharField(max_length=100, blank=True, null=True)
    Stage = models.CharField(max_length=100, blank=True, null=True)
    Evidence = models.TextField(blank=True, null=True)
    Note = models.TextField(blank=True, null=True)

    # New fields for more complete medical documentation
    Allergies = models.TextField(blank=True, null=True)  # Store patient allergy details
    Medications = models.TextField(blank=True, null=True)  # Active medication prescriptions
    Test_Results = models.TextField(blank=True, null=True)  # Lab tests or imaging reports

    def __str__(self):
        return f"Medical Record {self.RecordID} for {self.Patient.First_Name} {self.Patient.Last_Name}"


class Appointment(models.Model):
    AppointmentID = models.AutoField(primary_key=True)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Appointment_Date = models.DateTimeField()
    Doctor_Name = models.CharField(max_length=100)
    Notes = models.TextField(blank=True, null=True)
    Appointment_Status = models.CharField(max_length=10, choices=[('Completed', 'Completed'), ('Scheduled', 'Scheduled'), ('Cancelled', 'Cancelled')], default='Scheduled')

    def __str__(self):
        return f"Appointment {self.AppointmentID} - {self.Patient.First_Name}"

class Encounter(models.Model):
    EncounterID = models.AutoField(primary_key=True)
    Patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now_add=True)
    Notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Encounter {self.EncounterID} with {self.Patient}"


class Practitioner(models.Model):
    PractitionerID = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=15, blank=True, null=True)
    Specialization = models.CharField(max_length=255, blank=True, null=True)  # e.g., Cardiologist, Neurologist
    License_Number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    Address = models.TextField(blank=True, null=True)
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.First_Name} {self.Last_Name} - {self.Specialization or 'General'}"