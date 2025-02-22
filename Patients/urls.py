from django.urls import path
from . import views

urlpatterns = [
    path("", views.Dashboard, name="Dashboard"),
    path("patientList/", views.PatientList, name="PatientList"),
    path("appointment/", views.AppointmentView, name="Appointment"),
    path("medicalRecord/", views.MedicalRecordView, name="MedicalRecord"),
    path("fhirsync/", views.FHIRSync, name="FHIRSync"),
    path('newpatient/', views.AddPatient, name="AddPatient"),
    path('records/<str:patient_id>/', views.ViewRecords, name='view_records'),
    path('appointments/<str:patient_id>/', views.ViewAppointments, name='view_appointments'),
    path('edit/<str:patient_id>/', views.EditPatient, name='edit_patient'),
    path('delete/', views.DeletePatients, name='delete_patients'),
]