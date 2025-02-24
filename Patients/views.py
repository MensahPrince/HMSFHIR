from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Patient, MedicalRecord, Appointment
from .forms import PatientForm, AppointmentForm, AppointmentOnlyForms, MedicalRecordsForm
from django.http import HttpResponse

def Dashboard(request):
    appointments = Appointment.objects.all()  # Fetch all appointments
    context = {'Appointments': appointments}
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
                patient = patient_form.save(commit=True)
                appointment = appointment_form.save(commit=False)
                appointment.Patient = patient
                appointment.save()
                return redirect('PatientList')
            except IntegrityError as e:
                patient_form.add_error(None, f'Database error: {e}')
        print(patient_form.errors)
        print(appointment_form.errors)
    else:
        patient_form = PatientForm()
        appointment_form = AppointmentForm()

    return render(request, 'Patients/addpatient.html', {
        'patient_form': patient_form,
        'appointment_form': appointment_form
    })

def AddRecords(request):
    if request.method == 'POST':
        medicalrecords_form = MedicalRecordsForm(request.POST)
        if medicalrecords_form.is_valid():
            try:
                medicalrecords_form.save(commit=True)
                return redirect('MedicalRecord')
            except IntegrityError as e:
                medicalrecords_form.add_error(None, f'Database error: {e}')
        print(medicalrecords_form.errors)
    else:
        medicalrecords_form= MedicalRecordsForm()

    return render(request, 'Patients/addmedicalrecords.html', {
        'medicalrecords_form': medicalrecords_form
    })


def ViewRecordsSummary(request, patient_id):
    patient = get_object_or_404(Patient, PatientID=patient_id)
    appointments = Appointment.objects.filter(Patient=patient)
    medical_records = MedicalRecord.objects.filter(Patient=patient)
    context = {
        'patient': patient,
        'medical_records': medical_records,
        'appointments': appointments
    }
    return render(request, 'Patients/patientsummary.html', context)


def ViewRecords(request, patient_id):
    patient = get_object_or_404(Patient, PatientID=patient_id)
    appointments = Appointment.objects.filter(Patient=patient)
    medical_records = MedicalRecord.objects.filter(Patient=patient)
    context = {
        'patient': patient,
        'medical_records': medical_records,
    }
    return render(request, 'Patients/viewrecords.html', context)

def DeleteAppointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, AppointmentID=appointment_id)
    patient_id = appointment.Patient.PatientID
    appointment.delete()
    return redirect('view_summary', patient_id=patient_id)

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

def EditRecords(request, record_id):
    medical_record = get_object_or_404(MedicalRecord, RecordID=record_id)

    if request.method == 'POST':
        medicalrecords_form = MedicalRecordsForm(request.POST, instance=medical_record)
        if medicalrecords_form.is_valid():
            try:
                medicalrecords_form.save()
                return redirect('view_records', patient_id=medical_record.Patient.PatientID)
            except IntegrityError as e:
                medicalrecords_form.add_error(None, f'Database error: {e}')
    else:
        medicalrecords_form = MedicalRecordsForm(instance=medical_record)

    return render(request, 'Patients/editrecords.html', {
        'medicalrecords_form': medicalrecords_form,
        'medical_record': medical_record
    })

def DeletePatients(request):
    if request.method == 'POST':
        patient_ids = request.POST.getlist('patient_ids')
        Patient.objects.filter(PatientID__in=patient_ids).delete()
        return redirect('PatientList')

    return redirect('PatientList')

def ViewAppointments(request, patient_id):
    patient = get_object_or_404(Patient, PatientID=patient_id)
    appointments = Appointment.objects.filter(Patient=patient)
    context = {
        'patient': patient,
        'appointments': appointments  # Ensure the variable name is 'appointments'
    }
    return render(request, 'Patients/viewappointments.html', context)

def AddAppointment(request):
    if request.method == 'POST':
        form = AppointmentOnlyForms(request.POST)
        if form.is_valid():
            try:
                form.save()  # This saves the form data to the database
                return redirect('Appointment')  # Redirect to the list of patients after saving
            except IntegrityError:
                form.add_error(None, 'Database error')
    else:
        form = AppointmentOnlyForms()
    
    return render(request, 'Patients/addappointment.html', {'appointment_form': form})

'''''def viewRecords(request, patient_id):
    patient =  get_object_or_404(Patient, PatientID =patient_id)
    medicalrecords = MedicalRecord.objects.filter(Patient=patient)
    context = {
        'patient': patient,
        'medicalrecords' : medicalrecords
    }
    return render(request, 'Patients/viewrecords.html', context)'''''