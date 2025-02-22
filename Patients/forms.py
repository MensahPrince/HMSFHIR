from django import forms
from .models import Patient, Appointment

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
