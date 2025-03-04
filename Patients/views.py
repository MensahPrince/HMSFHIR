from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Patient, MedicalRecord, Appointment
from .forms import PatientForm, AppointmentForm, AppointmentOnlyForms, MedicalRecordsForm
from .fhir_service import get_patient, get_patient_condition, get_patient_with_condition
from django.views.decorators.csrf import csrf_exempt

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
#
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
    medical_records = patient.get_medical_records()

    # Fetch condition details from the database if available
    condition_details = 'No condition details available'
    if medical_records.exists():
        condition = medical_records.first()
        condition_details = {
            'id': condition.RecordID,
            'clinical_status': condition.Diagnosis,  # Assuming Diagnosis contains clinical status
            'verification_status': 'N/A',  # Update as needed
            'category': 'N/A',  # Update as needed
            'severity': 'N/A',  # Update as needed
            'code': condition.Diagnosis,  # Assuming Diagnosis contains the code
            'subject': patient.First_Name + ' ' + patient.Last_Name,
            'encounter': 'N/A',  # Update as needed
            'onset': 'N/A',  # Update as needed
            'abatement': 'N/A',  # Update as needed
            'recorded_date': condition.Date_Created,
            'recorder': 'N/A',  # Update as needed
            'asserter': 'N/A',  # Update as needed
            'stage': 'N/A',  # Update as needed
            'evidence': 'N/A',  # Update as needed
            'note': condition.Treatment  # Assuming Treatment contains notes
        }

    context = {
        'patient': patient,
        'medical_records': medical_records,
        'appointments': appointments,
        'condition_details': condition_details
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

def EditAppointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, AppointmentID=appointment_id)

    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST, instance=appointment)
        if appointment_form.is_valid():
            try:
                appointment_form.save()
                return redirect('view_appointments', patient_id=appointment.Patient.PatientID)
            except IntegrityError as e:
                appointment_form.add_error(None, f'Database error: {e}')
    else:
        appointment_form = AppointmentForm(instance=appointment)

    return render(request, 'Patients/editappointment.html', {
        'appointment_form': appointment_form,
        'appointment': appointment
    })

def PullPatient(request):
    if request.method == 'GET':
        patient_id = request.GET.get('patient_id')
        if patient_id:
            patient_data = get_patient_with_condition(patient_id)
            if patient_data:
                entry = patient_data.get('entry', [])
                if entry:
                    patient_entry = next((item for item in entry if item['resource']['resourceType'] == 'Patient'), None)
                    condition_entry = next((item for item in entry if item['resource']['resourceType'] == 'Condition'), None)

                    if patient_entry:
                        patient = patient_entry['resource']
                        condition = condition_entry['resource'] if condition_entry else None

                        condition_details = {
                            'id': condition.get('id', 'N/A'),
                            'clinical_status': condition.get('clinicalStatus', {}).get('coding', [{}])[0].get('display', 'N/A'),
                            'verification_status': condition.get('verificationStatus', {}).get('coding', [{}])[0].get('display', 'N/A'),
                            'category': condition.get('category', [{}])[0].get('coding', [{}])[0].get('display', 'N/A'),
                            'severity': condition.get('severity', {}).get('coding', [{}])[0].get('display', 'N/A'),
                            'code': condition.get('code', {}).get('coding', [{}])[0].get('display', 'N/A'),
                            'subject': condition.get('subject', {}).get('display', 'N/A'),
                            'encounter': condition.get('encounter', {}).get('reference', 'N/A'),
                            'onset': condition.get('onsetDateTime', 'N/A'),
                            'abatement': condition.get('abatementDateTime', 'N/A'),
                            'recorded_date': condition.get('recordedDate', 'N/A'),
                            'recorder': condition.get('recorder', {}).get('display', 'N/A'),
                            'asserter': condition.get('asserter', {}).get('display', 'N/A'),
                            'stage': condition.get('stage', [{}])[0].get('summary', {}).get('coding', [{}])[0].get('display', 'N/A'),
                            'evidence': condition.get('evidence', [{}])[0].get('detail', [{}])[0].get('display', 'N/A'),
                            'note': condition.get('note', [{}])[0].get('text', 'N/A')
                        } if condition else 'No condition details available'

                        context = {
                            'patient_id': patient.get('id', ''),
                            'identifier': patient.get('identifier', [{}])[0].get('value', ''),
                            'first_name': patient.get('name', [{}])[0].get('given', [''])[0],
                            'last_name': patient.get('name', [{}])[0].get('family', ''),
                            'birth_date': patient.get('birthDate', ''),
                            'gender': patient.get('gender', ''),
                            'address': patient.get('address', [{}])[0].get('text', ''),
                            'phone_number': patient.get('telecom', [{}])[0].get('value', ''),
                            'condition_details': condition_details
                        }
                        return render(request, 'Patients/pulledrecords.html', context)
            else:
                return render(request, 'Patients/pulledrecords.html', {'error': 'Patient not found'})
    return redirect('PatientList')


@csrf_exempt
def SavePulledPatient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        identifier = request.POST.get('identifier')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        condition_details = request.POST.get('condition_details')

        try:
            # Create or update the Patient object
            patient, created = Patient.objects.update_or_create(
                PatientID=patient_id,
                defaults={
                    'P_National_ID': identifier,
                    'First_Name': first_name,
                    'Last_Name': last_name,
                    'Date_of_Birth': birth_date,
                    'Gender': gender,
                    'Address': address,
                    'Phone_Number': phone_number
                }
            )

            # Save condition details to the database
            if condition_details and condition_details != 'No condition details available':
                MedicalRecord.objects.create(
                    Patient=patient,
                    Diagnosis=condition_details,
                    Treatment='N/A'  # You can update this as needed
                )

            return redirect('PatientList')
        except IntegrityError as e:
            return render(request, 'Patients/pulledrecords.html', {
                'error': f'Database error: {e}',
                'patient_id': patient_id,
                'identifier': identifier,
                'first_name': first_name,
                'last_name': last_name,
                'birth_date': birth_date,
                'gender': gender,
                'address': address,
                'phone_number': phone_number,
                'condition_details': condition_details
            })
    return redirect('PatientList')

def PullPatientCondition(request, patient_id):
    patient_data = get_patient_with_condition(patient_id)
    if patient_data:
        entry = patient_data.get('entry', [])
        if entry:
            patient_entry = next((item for item in entry if item['resource']['resourceType'] == 'Patient'), None)
            condition_entry = next((item for item in entry if item['resource']['resourceType'] == 'Condition'), None)

            if patient_entry:
                patient = patient_entry['resource']
                condition_details = condition_entry['resource'].get('code', {}).get('text', 'No condition details available') if condition_entry else 'No condition details available'

                context = {
                    'patient_id': patient.get('id', ''),
                    'identifier': patient.get('identifier', [{}])[0].get('value', ''),
                    'first_name': patient.get('name', [{}])[0].get('given', [''])[0],
                    'last_name': patient.get('name', [{}])[0].get('family', ''),
                    'birth_date': patient.get('birthDate', ''),
                    'gender': patient.get('gender', ''),
                    'address': patient.get('address', [{}])[0].get('text', ''),
                    'phone_number': patient.get('telecom', [{}])[0].get('value', ''),
                    'condition_details': condition_details
                }
                return render(request, 'Patients/pulledrecords.html', context)
    return render(request, 'Patients/pulledrecords.html', {'error': 'Patient not found'})