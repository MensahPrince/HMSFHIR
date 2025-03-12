import requests
from django.conf import settings

FHIR_BASE_URL = settings.HAPI_FHIR_BASE_URL

def get_patient(patient_id):
    """Fetch a patient by ID"""
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    response = requests.get(url, headers={"Accept": "application/fhir+json"})
    return response.json() if response.status_code == 200 else None

def search_patients(name):
    """Search patients by name"""
    url = f"{FHIR_BASE_URL}/Patient?name={name}"
    response = requests.get(url, headers={"Accept": "application/fhir+json"})
    return response.json() if response.status_code == 200 else None

def create_patient(patient_data):
    """Create a new patient"""
    url = f"{FHIR_BASE_URL}/Patient"
    headers = {"Content-Type": "application/fhir+json"}
    response = requests.post(url, json=patient_data, headers=headers)
    return response.json() if response.status_code in [200, 201] else None

def update_patient(patient_id, updated_data):
    """Update an existing patient"""
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    headers = {"Content-Type": "application/fhir+json"}
    response = requests.put(url, json=updated_data, headers=headers)
    return response.json() if response.status_code in [200, 201] else None

def delete_patient(patient_id):
    """Delete a patient"""
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    response = requests.delete(url)
    return response.status_code == 204

def get_patient_condition(patient_id):
    """Fetch a patient's condition by patient ID"""
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}/Condition"
    response = requests.get(url, headers={"Accept": "application/fhir+json"})
    return response.json() if response.status_code == 200 else None

def get_patient_with_condition(patient_id):
    """Fetch a patient by ID and include condition details"""
    url = f"{FHIR_BASE_URL}/Patient?_id={patient_id}&_revinclude=Condition:patient"
    response = requests.get(url, headers={"Accept": "application/fhir+json"})
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    patient = None
    condition_details = None
    
    for entry in data.get('entry', []):
        resource = entry.get('resource')
        if resource['resourceType'] == 'Patient':
            patient = {
                'PatientID': resource.get('id'),
                'P_National_ID': resource.get('identifier', [{}])[0].get('value', ''),
                'First_Name': resource.get('name', [{}])[0].get('given', [''])[0],
                'Last_Name': resource.get('name', [{}])[0].get('family', ''),
                'Date_of_Birth': resource.get('birthDate', ''),
                'Gender': resource.get('gender', ''),
                'Address': resource.get('address', [{}])[0].get('text', ''),
                'Phone_Number': resource.get('telecom', [{}])[0].get('value', '')
            }
        elif resource['resourceType'] == 'Condition':
            condition_details = {
                'id': resource.get('id', ''),
                'clinical_status': resource.get('clinicalStatus', {}).get('text', ''),
                'verification_status': resource.get('verificationStatus', {}).get('text', ''),
                'category': resource.get('category', [{}])[0].get('text', ''),
                'severity': resource.get('severity', {}).get('text', ''),
                'code': resource.get('code', {}).get('text', ''),
                'subject': resource.get('subject', {}).get('reference', ''),
                'encounter': resource.get('encounter', {}).get('reference', ''),
                'onset': resource.get('onsetDateTime', ''),
                'abatement': resource.get('abatementDateTime', ''),
                'recorded_date': resource.get('recordedDate', ''),
                'recorder': resource.get('recorder', {}).get('reference', ''),
                'asserter': resource.get('asserter', {}).get('reference', ''),
                'stage': resource.get('stage', [{}])[0].get('summary', {}).get('text', ''),
                'evidence': resource.get('evidence', [{}])[0].get('detail', [{}])[0].get('display', ''),
                'note': resource.get('note', [{}])[0].get('text', '')
            }
    
    return {'patient': patient, 'condition_details': condition_details}
