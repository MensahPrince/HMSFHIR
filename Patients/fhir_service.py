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
