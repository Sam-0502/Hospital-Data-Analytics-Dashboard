import os
import pandas as pd

def create_sample_templates():
    samples_dir = os.path.join("data", "samples")
    os.makedirs(samples_dir, exist_ok=True)

    # Patients Sample
    df_patients = pd.DataFrame([
        {
            "patient_id": "P001",
            "first_name": "David",
            "last_name": "Williams",
            "gender": "Male",
            "date_of_birth": "1985-04-12",
            "contact_number": "+91-9876543210",
            "address": "123 Main Street, Sector 4",
            "registration_date": "2024-01-15",
            "insurance_provider": "Star Health",
            "insurance_number": "INS840674",
            "email": "david.williams@mail.com"
        },
        {
            "patient_id": "P002",
            "first_name": "Emily",
            "last_name": "Smith",
            "gender": "Female",
            "date_of_birth": "1992-08-22",
            "contact_number": "+91-9876543211",
            "address": "456 Park Avenue, Flat 3B",
            "registration_date": "2024-02-01",
            "insurance_provider": "HDFC ERGO",
            "insurance_number": "INS354079",
            "email": "emily.smith@mail.com"
        }
    ])
    df_patients.to_csv(os.path.join(samples_dir, "sample_patients.csv"), index=False)

    # Doctors Sample
    df_doctors = pd.DataFrame([
        {
            "doctor_id": "D001",
            "first_name": "David",
            "last_name": "Taylor",
            "specialization": "Cardiology",
            "phone_number": "+91-9811100001",
            "years_experience": 15,
            "hospital_branch": "Westside Clinic",
            "email": "dr.david.taylor@hospital.com"
        },
        {
            "doctor_id": "D002",
            "first_name": "Jane",
            "last_name": "Davis",
            "specialization": "Neurology",
            "phone_number": "+91-9811100002",
            "years_experience": 12,
            "hospital_branch": "Eastside Clinic",
            "email": "dr.jane.davis@hospital.com"
        }
    ])
    df_doctors.to_csv(os.path.join(samples_dir, "sample_doctors.csv"), index=False)

    # Appointments Sample
    df_appointments = pd.DataFrame([
        {
            "appointment_id": "A001",
            "patient_id": "P001",
            "doctor_id": "D001",
            "appointment_date": "2024-03-10",
            "appointment_time": "10:30:00",
            "reason_for_visit": "Therapy",
            "status": "Completed"
        },
        {
            "appointment_id": "A002",
            "patient_id": "P002",
            "doctor_id": "D002",
            "appointment_date": "2024-03-11",
            "appointment_time": "14:00:00",
            "reason_for_visit": "Consultation",
            "status": "Scheduled"
        }
    ])
    df_appointments.to_csv(os.path.join(samples_dir, "sample_appointments.csv"), index=False)

    # Treatments Sample
    df_treatments = pd.DataFrame([
        {
            "treatment_id": "T001",
            "appointment_id": "A001",
            "treatment_type": "Cardiovascular Stenting",
            "description": "Coronary artery stent insertion",
            "cost": 3941.97,
            "treatment_date": "2024-03-10"
        },
        {
            "treatment_id": "T002",
            "appointment_id": "A002",
            "treatment_type": "Neurological Consultation",
            "description": "Brain MRI review and medication",
            "cost": 1500.00,
            "treatment_date": "2024-03-11"
        }
    ])
    df_treatments.to_csv(os.path.join(samples_dir, "sample_treatments.csv"), index=False)

    # Billing Sample
    df_billing = pd.DataFrame([
        {
            "bill_id": "B001",
            "patient_id": "P001",
            "treatment_id": "T001",
            "bill_date": "2024-03-10",
            "amount": 3941.97,
            "payment_method": "Insurance",
            "payment_status": "Paid"
        },
        {
            "bill_id": "B002",
            "patient_id": "P002",
            "treatment_id": "T002",
            "bill_date": "2024-03-11",
            "amount": 1500.00,
            "payment_method": "Credit Card",
            "payment_status": "Pending"
        }
    ])
    df_billing.to_csv(os.path.join(samples_dir, "sample_billing.csv"), index=False)

    print("[OK] Sample CSV templates created successfully in data/samples/")

if __name__ == "__main__":
    create_sample_templates()
