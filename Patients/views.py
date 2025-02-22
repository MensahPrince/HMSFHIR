from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Patient, MedicalRecord, Appointment
from .forms import PatientForm, AppointmentForm

def Dashboard(request):
    Appointments = Appointment.objects.all()
    context = {'Appointments': Appointments}
    return render(request, "Patients/dashboard.html", context)

def PatientList(request):
    Patients = Patient.objects.all()
    context = {'Patients': Patients}
    return render(request, 'Patients/patientList.html', context)

def AppointmentView(request):
    Appointments = Appointment.objects.all()
    context = {'Appointments' : Appointments }
    return render(request, "Patients/appointments.html", context)

def MedicalRecordView(request):
    MedicalRecords = MedicalRecord.objects.all()
    context = {"MedicalRecords": MedicalRecords}
    return render(request, "Patients/medicalrecord.html", context)

def FHIRSync(request):
    context = {}
    return render(request, "Patients/fhirsync.html", context)

def AddPatient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        appointment_form = AppointmentForm(request.POST)

        if patient_form.is_valid() and appointment_form.is_valid():
            try:
                # First, create and save the patient
                patient = patient_form.save(commit=True)  # Save patient immediately
                
                # Now, create and save the appointment linked to the patient
                appointment = appointment_form.save(commit=False)
                appointment.Patient = patient  # Link to saved patient
                appointment.save()

                return redirect('PatientList')

            except IntegrityError as e:
                patient_form.add_error(None, f'Database error: {e}')
        
        # Print form errors for debugging
        print(patient_form.errors)
        print(appointment_form.errors)

    else:
        patient_form = PatientForm()
        appointment_form = AppointmentForm()

    return render(request, 'Patients/addpatient.html', {
        'patient_form': patient_form,
        'appointment_form': appointment_form
    })

def ViewRecords(request, patient_id):
    patient = get_object_or_404(Patient, PatientID=patient_id)
    medical_records = MedicalRecord.objects.filter(Patient=patient)
    context = {
        'patient': patient,
        'medical_records': medical_records
    }
    return render(request, 'Patients/viewrecords.html', context)

def EditPatient(request, patient_id):
    patient = get_object_or_404(Patient, PatientID=patient_id)

    if request.method == 'POST':
        patient_form = PatientForm(request.POST, instance=patient)
        if patient_form.is_valid():
            try:
                patient_form.save()
                return redirect('PatientList')
            except IntegrityError as e:
                patient_form.add_error(None, f'Database error: {e}')
    else:
        patient_form = PatientForm(instance=patient)

    return render(request, 'Patients/editpatient.html', {
        'patient_form': patient_form,
        'patient': patient
    })

def DeletePatients(request):
    if request.method == 'POST':
        patient_ids = request.POST.getlist('patient_ids')
        Patient.objects.filter(PatientID__in=patient_ids).delete()
        return redirect('PatientList')

    return redirect('PatientList')

