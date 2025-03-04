from django import forms
from .models import Patient, Appointment, MedicalRecord

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['PatientID', 'P_National_ID', 'First_Name', 'Last_Name', 'Date_of_Birth', 'Gender', 'Address', 'Phone_Number']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['Appointment_Status', 'Appointment_Date', 'Doctor_Name', 'Notes']

class AppointmentOnlyForms(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['Patient', 'Appointment_Status', 'Appointment_Date', 'Doctor_Name', 'Notes']

class MedicalRecordsForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            'Patient', 'Diagnosis', 'Treatment', 'Clinical_Status', 'Verification_Status', 'Category', 
            'Severity', 'Code', 'Subject', 'Encounter', 'Onset', 'Abatement', 'Recorded_Date', 
            'Recorder', 'Asserter', 'Stage', 'Evidence', 'Note'
        ]