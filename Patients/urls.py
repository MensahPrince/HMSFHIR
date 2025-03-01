from django.urls import path
from . import views

urlpatterns = [
    path("", views.Dashboard, name="Dashboard"),
    path("patientList/", views.PatientList, name="PatientList"),
    path("appointment/", views.AppointmentView, name="Appointment"),
    path("medicalRecord/", views.MedicalRecordView, name="MedicalRecord"),
    path("fhirsync/", views.FHIRSync, name="FHIRSync"),
    path('newpatient/', views.AddPatient, name="AddPatient"),
    path('newrecord/', views.AddRecords, name="Addrecords"),
    path('records/<str:patient_id>/', views.ViewRecords, name='view_records'),
    path('summary/<str:patient_id>/', views.ViewRecordsSummary, name='view_summary'),
    path('appointments/<str:patient_id>/', views.ViewAppointments, name='view_appointments'),
    path('edit/<str:patient_id>/', views.EditPatient, name='edit_patient'),
    path('delete/', views.DeletePatients, name='delete_patients'),
    path('addappointment/', views.AddAppointment, name='add_appointment'),
    path('deleteappointment/<int:appointment_id>/', views.DeleteAppointment, name='delete_appointment'),  # Added delete appointment URL
    #path('view_medicalrecords/<str:patient_id>', views.viewRecords, name="viewRecords")
    path('editrecord/<int:record_id>/', views.EditRecords, name='edit_record'),
    path('editappointment/<int:appointment_id>/', views.EditAppointment, name='edit_appointment'),
    path('pullpatient/', views.PullPatient, name='pull_patient'),  # Added pull patient URL
]
