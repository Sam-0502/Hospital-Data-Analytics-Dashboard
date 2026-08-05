import pandas as pd
import json
import os

def run_etl():
    data_dir = "data"
    
    # Read the 5 uploaded CSV files
    df_patients = pd.read_csv(os.path.join(data_dir, "patients.csv"))
    df_doctors = pd.read_csv(os.path.join(data_dir, "doctors.csv"))
    df_appointments = pd.read_csv(os.path.join(data_dir, "appointments.csv"))
    df_treatments = pd.read_csv(os.path.join(data_dir, "treatments.csv"))
    df_billing = pd.read_csv(os.path.join(data_dir, "billing.csv"))

    print(f"Loaded Patients: {len(df_patients)} rows")
    print(f"Loaded Doctors: {len(df_doctors)} rows")
    print(f"Loaded Appointments: {len(df_appointments)} rows")
    print(f"Loaded Treatments: {len(df_treatments)} rows")
    print(f"Loaded Billing: {len(df_billing)} rows")

    # Clean records
    patients = df_patients.fillna("").to_dict(orient="records")
    doctors = df_doctors.fillna("").to_dict(orient="records")
    appointments = df_appointments.fillna("").to_dict(orient="records")
    treatments = df_treatments.fillna("").to_dict(orient="records")
    billing = df_billing.fillna("").to_dict(orient="records")

    # Combine into JSON object for web dashboard
    master_json = {
        "patients": patients,
        "doctors": doctors,
        "appointments": appointments,
        "treatments": treatments,
        "billing": billing
    }

    with open(os.path.join(data_dir, "hospital_data.json"), "w", encoding="utf-8") as f:
        json.dump(master_json, f, indent=2)
    print("[OK] Successfully generated data/hospital_data.json from uploaded CSV files!")

    # Write SQL Insert script
    sql_path = os.path.join("sql", "02_data_inserts.sql")
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("-- HOSPITAL DATA ANALYTICS INSERTS (DERIVED FROM UPLOADED CSV DATASETS)\nUSE hospital_analytics_db;\n\n")

        # Patients
        f.write("-- 1. PATIENTS INSERTS\n")
        for p in patients:
            fn = str(p['first_name']).replace("'", "''")
            ln = str(p['last_name']).replace("'", "''")
            addr = str(p['address']).replace("'", "''")
            prov = str(p['insurance_provider']).replace("'", "''")
            f.write(f"INSERT INTO patients (patient_id, first_name, last_name, gender, date_of_birth, contact_number, address, registration_date, insurance_provider, insurance_number, email) VALUES ('{p['patient_id']}', '{fn}', '{ln}', '{p['gender']}', '{p['date_of_birth']}', '{p['contact_number']}', '{addr}', '{p['registration_date']}', '{prov}', '{p['insurance_number']}', '{p['email']}');\n")

        # Doctors
        f.write("\n-- 2. DOCTORS INSERTS\n")
        for d in doctors:
            fn = str(d['first_name']).replace("'", "''")
            ln = str(d['last_name']).replace("'", "''")
            spec = str(d['specialization']).replace("'", "''")
            branch = str(d['hospital_branch']).replace("'", "''")
            f.write(f"INSERT INTO doctors (doctor_id, first_name, last_name, specialization, phone_number, years_experience, hospital_branch, email) VALUES ('{d['doctor_id']}', '{fn}', '{ln}', '{spec}', '{d['phone_number']}', {d['years_experience']}, '{branch}', '{d['email']}');\n")

        # Appointments
        f.write("\n-- 3. APPOINTMENTS INSERTS\n")
        for a in appointments:
            reason = str(a['reason_for_visit']).replace("'", "''")
            f.write(f"INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit, status) VALUES ('{a['appointment_id']}', '{a['patient_id']}', '{a['doctor_id']}', '{a['appointment_date']}', '{a['appointment_time']}', '{reason}', '{a['status']}');\n")

        # Treatments
        f.write("\n-- 4. TREATMENTS INSERTS\n")
        for t in treatments:
            ttype = str(t['treatment_type']).replace("'", "''")
            desc = str(t['description']).replace("'", "''")
            f.write(f"INSERT INTO treatments (treatment_id, appointment_id, treatment_type, description, cost, treatment_date) VALUES ('{t['treatment_id']}', '{t['appointment_id']}', '{ttype}', '{desc}', {t['cost']}, '{t['treatment_date']}');\n")

        # Billing
        f.write("\n-- 5. BILLING INSERTS\n")
        for b in billing:
            f.write(f"INSERT INTO billing (bill_id, patient_id, treatment_id, bill_date, amount, payment_method, payment_status) VALUES ('{b['bill_id']}', '{b['patient_id']}', '{b['treatment_id']}', '{b['bill_date']}', {b['amount']}, '{b['payment_method']}', '{b['payment_status']}');\n")

    print("[OK] Successfully generated sql/02_data_inserts.sql!")

if __name__ == "__main__":
    run_etl()
