import json
import random
from datetime import datetime, timedelta

random.seed(42)

# Master static reference data
BRANCHES = [
    {"branch_id": 1, "branch_name": "Apex Central Hospital", "city": "Mumbai", "state": "Maharashtra", "zip_code": "400001", "phone": "+91-22-5551001", "total_beds": 120, "established_year": 2010},
    {"branch_id": 2, "branch_name": "Metro Health Institute", "city": "Bengaluru", "state": "Karnataka", "zip_code": "560001", "phone": "+91-80-5552002", "total_beds": 150, "established_year": 2012},
    {"branch_id": 3, "branch_name": "CareFirst Super Specialty", "city": "Delhi", "state": "Delhi", "zip_code": "110001", "phone": "+91-11-5553003", "total_beds": 180, "established_year": 2015},
    {"branch_id": 4, "branch_name": "Sunrise Medical Center", "city": "Hyderabad", "state": "Telangana", "zip_code": "500001", "phone": "+91-40-5554004", "total_beds": 90, "established_year": 2018},
    {"branch_id": 5, "branch_name": "St. Jude General Hospital", "city": "Chennai", "state": "Tamil Nadu", "zip_code": "600001", "phone": "+91-44-5555005", "total_beds": 110, "established_year": 2014}
]

DEPARTMENTS = [
    {"department_id": 1, "department_name": "Cardiology", "department_head": "Dr. Rajesh Sharma", "floor_number": 3, "annual_budget": 1200000.00},
    {"department_id": 2, "department_name": "Neurology", "department_head": "Dr. Ananya Roy", "floor_number": 4, "annual_budget": 950000.00},
    {"department_id": 3, "department_name": "Orthopedics", "department_head": "Dr. Vikram Seth", "floor_number": 2, "annual_budget": 850000.00},
    {"department_id": 4, "department_name": "Oncology", "department_head": "Dr. Sunita Patel", "floor_number": 5, "annual_budget": 1500000.00},
    {"department_id": 5, "department_name": "Pediatrics", "department_head": "Dr. Ramesh Gupta", "floor_number": 1, "annual_budget": 600000.00},
    {"department_id": 6, "department_name": "General Medicine", "department_head": "Dr. Priya Nair", "floor_number": 1, "annual_budget": 700000.00},
    {"department_id": 7, "department_name": "Dermatology", "department_head": "Dr. Arvind Menon", "floor_number": 2, "annual_budget": 450000.00},
    {"department_id": 8, "department_name": "Emergency Care", "department_head": "Dr. Sanjay Verma", "floor_number": 1, "annual_budget": 1100000.00}
]

DOCTORS_SPEC = [
    ("Dr. Rajesh", "Sharma", "Male", "rajesh.sharma@hospital.com", "Cardiology", 1, 1, 18, 1500.00, "MD, DM (Cardiology)"),
    ("Dr. Meera", "Deshmukh", "Female", "meera.d@hospital.com", "Cardiology", 1, 2, 12, 1200.00, "MD, DNB"),
    ("Dr. Ananya", "Roy", "Female", "ananya.roy@hospital.com", "Neurology", 2, 2, 15, 1600.00, "MD, DM (Neurology)"),
    ("Dr. Amit", "Kulkarni", "Male", "amit.k@hospital.com", "Neurology", 2, 3, 10, 1300.00, "MD (Neurology)"),
    ("Dr. Vikram", "Seth", "Male", "vikram.seth@hospital.com", "Orthopedics", 3, 1, 20, 1400.00, "MS (Ortho), FRCS"),
    ("Dr. Kavita", "Joshi", "Female", "kavita.j@hospital.com", "Orthopedics", 3, 4, 8, 1000.00, "MS (Ortho)"),
    ("Dr. Sunita", "Patel", "Female", "sunita.patel@hospital.com", "Oncology", 4, 3, 22, 2000.00, "MD, DM (Oncology)"),
    ("Dr. Siddharth", "Rao", "Male", "siddharth.r@hospital.com", "Oncology", 4, 5, 9, 1500.00, "MD (Oncology)"),
    ("Dr. Ramesh", "Guptan", "Male", "ramesh.g@hospital.com", "Pediatrics", 5, 4, 16, 900.00, "MD (Pediatrics)"),
    ("Dr. Sneha", "Iyer", "Female", "sneha.iyer@hospital.com", "Pediatrics", 5, 2, 7, 800.00, "DCH, MD"),
    ("Dr. Priya", "Nair", "Female", "priya.nair@hospital.com", "General Medicine", 6, 1, 14, 850.00, "MD (General Medicine)"),
    ("Dr. Alok", "Verma", "Male", "alok.v@hospital.com", "General Medicine", 6, 5, 11, 800.00, "MD (Medicine)"),
    ("Dr. Arvind", "Menon", "Male", "arvind.m@hospital.com", "Dermatology", 7, 2, 13, 1100.00, "MD (Dermatology)"),
    ("Dr. Deepa", "Shah", "Female", "deepa.s@hospital.com", "Dermatology", 7, 3, 6, 950.00, "DVD, MD"),
    ("Dr. Sanjay", "Verma", "Male", "sanjay.v@hospital.com", "Emergency Care", 8, 1, 17, 1350.00, "MD (Emergency Medicine)"),
    ("Dr. Pooja", "Bhatia", "Female", "pooja.b@hospital.com", "Emergency Care", 8, 4, 9, 1100.00, "MEM, MBBS")
]

DISEASES = [
    {"disease_id": 1, "disease_name": "Hypertension", "category": "Cardiovascular", "severity_level": "Moderate", "icd_code": "I10", "description": "High blood pressure condition"},
    {"disease_id": 2, "disease_name": "Ischemic Heart Disease", "category": "Cardiovascular", "severity_level": "High", "icd_code": "I25", "description": "Coronary artery disease"},
    {"disease_id": 3, "disease_name": "Type 2 Diabetes Mellitus", "category": "Endocrine", "severity_level": "Moderate", "icd_code": "E11", "description": "Chronic metabolic disorder"},
    {"disease_id": 4, "disease_name": "Acute Appendicitis", "category": "Gastrointestinal", "severity_level": "High", "icd_code": "K35", "description": "Inflammation of the appendix"},
    {"disease_id": 5, "disease_name": "Osteoarthritis", "category": "Musculoskeletal", "severity_level": "Moderate", "icd_code": "M19", "description": "Degenerative joint disease"},
    {"disease_id": 6, "disease_name": "Asthma Exacerbation", "category": "Respiratory", "severity_level": "Moderate", "icd_code": "J45", "description": "Airway constriction disease"},
    {"disease_id": 7, "disease_name": "Community Acquired Pneumonia", "category": "Respiratory", "severity_level": "High", "icd_code": "J18", "description": "Lung infection"},
    {"disease_id": 8, "disease_name": "Migraine Headache", "category": "Neurological", "severity_level": "Low", "icd_code": "G43", "description": "Severe recurrent headache"},
    {"disease_id": 9, "disease_name": "Breast Carcinoma", "category": "Oncology", "severity_level": "Critical", "icd_code": "C50", "description": "Malignant neoplasm of breast"},
    {"disease_id": 10, "disease_name": "Kidney Stones (Nephrolithiasis)", "category": "Urology", "severity_level": "Moderate", "icd_code": "N20", "description": "Mineral deposits in kidneys"}
]

MEDICINES = [
    {"medicine_id": 1, "medicine_name": "Atorvastatin 10mg", "manufacturer": "Cipla", "unit_cost": 15.50, "stock_quantity": 500, "category": "Cardiovascular"},
    {"medicine_id": 2, "medicine_name": "Metformin 500mg", "manufacturer": "Sun Pharma", "unit_cost": 8.00, "stock_quantity": 800, "category": "Antidiabetic"},
    {"medicine_id": 3, "medicine_name": "Amoxicillin 500mg", "manufacturer": "Reddy's", "unit_cost": 12.00, "stock_quantity": 600, "category": "Antibiotic"},
    {"medicine_id": 4, "medicine_name": "Paracetamol 650mg", "manufacturer": "GSK", "unit_cost": 3.50, "stock_quantity": 1200, "category": "Analgesic"},
    {"medicine_id": 5, "medicine_name": "Pantoprazole 40mg", "manufacturer": "Torrent", "unit_cost": 9.50, "stock_quantity": 700, "category": "Gastrointestinal"},
    {"medicine_id": 6, "medicine_name": "Amlodipine 5mg", "manufacturer": "Lupin", "unit_cost": 6.00, "stock_quantity": 900, "category": "Cardiovascular"},
    {"medicine_id": 7, "medicine_name": "Montelukast 10mg", "manufacturer": "Glenmark", "unit_cost": 18.00, "stock_quantity": 400, "category": "Respiratory"},
    {"medicine_id": 8, "medicine_name": "Ceftriaxone 1g Inj", "manufacturer": "Cipla", "unit_cost": 140.00, "stock_quantity": 250, "category": "Injectable Antibiotic"}
]

FIRST_NAMES_MALE = ["Aarav", "Rohan", "Kabir", "Aditya", "Vihaan", "Karan", "Nikhil", "Manish", "Varun", "Suresh", "Ramesh", "Deepak", "Sunil", "Anil", "Amit", "Gaurav", "Harsh", "Kunal", "Rahul", "Vikas"]
FIRST_NAMES_FEMALE = ["Ananya", "Diya", "Isha", "Riya", "Kavya", "Pooja", "Neha", "Shreya", "Anushka", "Priya", "Sunita", "Anita", "Geeta", "Meena", "Suman", "Divya", "Kirti", "Swati", "Rashmi", "Sonam"]
LAST_NAMES = ["Sharma", "Verma", "Gupta", "Patel", "Shah", "Joshi", "Kulkarni", "Deshmukh", "Nair", "Menon", "Reddy", "Rao", "Chowdhury", "Das", "Banerjee", "Singh", "Yadav", "Kumar", "Mishra", "Pandey"]
CITIES = ["Mumbai", "Bengaluru", "Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad"]

def generate_dataset():
    # Doctors
    doctors = []
    for idx, d in enumerate(DOCTORS_SPEC, 1):
        doctors.append({
            "doctor_id": idx,
            "first_name": d[0],
            "last_name": d[1],
            "gender": d[2],
            "email": d[3],
            "phone": f"+91-98765{idx:05d}",
            "specialization": d[4],
            "department_id": d[5],
            "branch_id": d[6],
            "experience_years": d[7],
            "consultation_fee": d[8],
            "qualification": d[9],
            "joining_date": f"201{random.randint(2,9)}-0{random.randint(1,9)}-15"
        })

    # Patients (300 patients)
    patients = []
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    for idx in range(1, 301):
        gender = random.choice(["Male", "Female"])
        fn = random.choice(FIRST_NAMES_MALE if gender == "Male" else FIRST_NAMES_FEMALE)
        ln = random.choice(LAST_NAMES)
        dob_year = random.randint(1950, 2018)
        dob_month = random.randint(1, 12)
        dob_day = random.randint(1, 28)
        reg_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 750))
        
        patients.append({
            "patient_id": idx,
            "first_name": fn,
            "last_name": ln,
            "gender": gender,
            "dob": f"{dob_year}-{dob_month:02d}-{dob_day:02d}",
            "phone": f"+91-91234{idx:05d}",
            "email": f"{fn.lower()}.{ln.lower()}{idx}@mail.com",
            "address": f"Flat {random.randint(101,909)}, Sector {random.randint(1,50)}",
            "city": random.choice(CITIES),
            "state": "Maharashtra",
            "blood_group": random.choice(blood_groups),
            "emergency_contact": f"+91-98111{idx:05d}",
            "registration_date": reg_date.strftime("%Y-%m-%d")
        })

    # Insurance
    insurances = []
    providers = ["Star Health", "HDFC ERGO", "ICICI Lombard", "Max Bupa", "Care Health", "SBI General"]
    for idx, p in enumerate(patients[:200], 1): # 200 patients insured
        insurances.append({
            "insurance_id": idx,
            "patient_id": p["patient_id"],
            "provider_name": random.choice(providers),
            "policy_number": f"POL-2024-{idx:05d}",
            "coverage_limit": random.choice([300000.00, 500000.00, 1000000.00]),
            "copay_percentage": random.choice([10.0, 15.0, 20.0]),
            "status": "Active",
            "expiry_date": "2027-12-31"
        })

    # Appointments (600 appointments over 2024-2026)
    appointments = []
    statuses = ["Completed"] * 75 + ["Cancelled"] * 15 + ["No Show"] * 10
    app_types = ["Consultation", "Follow-up", "Routine Checkup", "Emergency", "Procedure"]
    
    start_date = datetime(2024, 1, 1)
    for idx in range(1, 601):
        p = random.choice(patients)
        doc = random.choice(doctors)
        app_date = start_date + timedelta(days=random.randint(0, 930)) # up to middle of 2026
        hour = random.choice([8, 9, 10, 11, 14, 15, 16, 17, 18, 19])
        minute = random.choice([0, 15, 30, 45])
        st = random.choice(statuses)
        wt = random.randint(5, 60) if st == "Completed" else 0
        
        appointments.append({
            "appointment_id": idx,
            "patient_id": p["patient_id"],
            "doctor_id": doc["doctor_id"],
            "department_id": doc["department_id"],
            "branch_id": doc["branch_id"],
            "appointment_date": app_date.strftime("%Y-%m-%d"),
            "appointment_time": f"{hour:02d}:{minute:02d}:00",
            "status": st,
            "appointment_type": random.choice(app_types),
            "waiting_time_minutes": wt
        })

    # Treatments & Billing for Completed Appointments
    treatments = []
    billings = []
    t_idx = 1
    b_idx = 1
    
    completed_apps = [a for a in appointments if a["status"] == "Completed"]
    
    treatment_names = [
        "Cardiovascular Stenting", "Hypertension Management Protocol", "Insulin Therapy & Diet Plan",
        "Laparoscopic Appendectomy", "Total Knee Replacement", "Nebulization & Inhaler Therapy",
        "IV Antibiotics Course", "Migraine Relief Therapy", "Targeted Chemotherapy Session", "Laser Lithotripsy"
    ]
    
    for app in completed_apps:
        doc = next(d for d in doctors if d["doctor_id"] == app["doctor_id"])
        disease = random.choice(DISEASES)
        t_cost = round(doc["consultation_fee"] + random.uniform(500, 15000), 2)
        success = random.choice(["Successful"] * 85 + ["In Progress"] * 10 + ["Complication"] * 5)
        
        treatments.append({
            "treatment_id": t_idx,
            "appointment_id": app["appointment_id"],
            "patient_id": app["patient_id"],
            "doctor_id": app["doctor_id"],
            "disease_id": disease["disease_id"],
            "treatment_name": random.choice(treatment_names),
            "treatment_date": app["appointment_date"],
            "treatment_cost": t_cost,
            "success_status": success,
            "duration_days": random.randint(1, 10)
        })
        
        # Billing calculation
        total_amt = round(t_cost + random.uniform(200, 2000), 2)
        ins = next((i for i in insurances if i["patient_id"] == app["patient_id"]), None)
        
        if ins and random.random() < 0.7:
            ins_id = ins["insurance_id"]
            ins_covered = round(total_amt * (1 - (ins["copay_percentage"]/100)), 2)
            patient_paid = round(total_amt - ins_covered, 2)
            p_status = "Completed"
            p_method = "Insurance"
        else:
            ins_id = None
            ins_covered = 0.00
            if random.random() < 0.85:
                patient_paid = total_amt
                p_status = "Completed"
            else:
                patient_paid = round(total_amt * 0.5, 2)
                p_status = "Partially Paid"
            p_method = random.choice(["Credit Card", "Debit Card", "Cash", "UPI", "Net Banking"])

        billings.append({
            "bill_id": b_idx,
            "patient_id": app["patient_id"],
            "appointment_id": app["appointment_id"],
            "treatment_id": t_idx,
            "insurance_id": ins_id,
            "total_amount": total_amt,
            "insurance_covered": ins_covered,
            "patient_paid": patient_paid,
            "pending_amount": round(total_amt - ins_covered - patient_paid, 2),
            "payment_status": p_status,
            "payment_method": p_method,
            "billing_date": app["appointment_date"]
        })
        
        t_idx += 1
        b_idx += 1

    # Rooms & Beds (100 beds)
    rooms = []
    room_types = ["General Ward", "Semi-Private", "Private ICU", "Deluxe", "CCU"]
    rates = {"General Ward": 1500.0, "Semi-Private": 3500.0, "Private ICU": 8000.0, "Deluxe": 6000.0, "CCU": 10000.0}
    for idx in range(1, 101):
        rt = random.choice(room_types)
        branch = random.choice(BRANCHES)
        st = random.choice(["Occupied", "Available", "Available", "Under Maintenance"])
        p_assigned = random.choice(patients)["patient_id"] if st == "Occupied" else None
        rooms.append({
            "room_id": idx,
            "branch_id": branch["branch_id"],
            "room_number": f"R-{100+idx}",
            "room_type": rt,
            "daily_rate": rates[rt],
            "status": st,
            "assigned_patient_id": p_assigned
        })

    # Emergency Visits (150 visits)
    emergencies = []
    triage_levels = ['Level 1 - Resuscitation', 'Level 2 - Emergent', 'Level 3 - Urgent', 'Level 4 - Less Urgent', 'Level 5 - Non-Urgent']
    outcomes = ['Admitted', 'Discharged', 'Discharged', 'Transferred', 'Deceased']
    for idx in range(1, 151):
        p = random.choice(patients)
        branch = random.choice(BRANCHES)
        doc = random.choice([d for d in doctors if d["department_id"] in [1, 8]]) # Emergency/Cardiology
        arr_time = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 900), hours=random.randint(0,23), minutes=random.randint(0,59))
        dis_time = arr_time + timedelta(hours=random.randint(2, 48))
        emergencies.append({
            "emergency_id": idx,
            "patient_id": p["patient_id"],
            "branch_id": branch["branch_id"],
            "doctor_id": doc["doctor_id"],
            "arrival_time": arr_time.strftime("%Y-%m-%d %H:%M:%S"),
            "triage_level": random.choice(triage_levels),
            "discharge_time": dis_time.strftime("%Y-%m-%d %H:%M:%S"),
            "outcome": random.choice(outcomes)
        })

    # Patient Feedback (200 feedback entries)
    feedbacks = []
    reviews = [
        "Excellent care and compassionate doctors.", "Long wait time but treatment was effective.",
        "Clean facilities and very polite nursing staff.", "Dr. Sharma was extremely thorough and knowledgeable.",
        "Billing took longer than expected but clean hospital.", "Highly satisfied with pediatric department care.",
        "State of the art equipment and seamless registration.", "Average experience, waiting area was crowded."
    ]
    for idx in range(1, 201):
        app = random.choice(completed_apps)
        rating = random.choice([5, 5, 4, 4, 4, 3, 2, 1])
        feedbacks.append({
            "feedback_id": idx,
            "patient_id": app["patient_id"],
            "doctor_id": app["doctor_id"],
            "appointment_id": app["appointment_id"],
            "rating": rating,
            "cleanliness_rating": random.choice([4, 5, 5, 3]),
            "staff_courtesy_rating": random.choice([4, 5, 5, 4]),
            "review_text": random.choice(reviews),
            "feedback_date": app["appointment_date"]
        })

    return {
        "branches": BRANCHES,
        "departments": DEPARTMENTS,
        "doctors": doctors,
        "patients": patients,
        "insurance": insurances,
        "disease_categories": DISEASES,
        "appointments": appointments,
        "treatments": treatments,
        "billing": billings,
        "medicines": MEDICINES,
        "rooms_beds": rooms,
        "emergency_visits": emergencies,
        "patient_feedback": feedbacks
    }

if __name__ == "__main__":
    data = generate_dataset()
    
    # Save as JSON for frontend web application
    with open("data/hospital_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("[OK] Successfully generated data/hospital_data.json")

    # Generate SQL insert script
    with open("sql/02_data_inserts.sql", "w", encoding="utf-8") as f:
        f.write("-- HOSPITAL DATA ANALYTICS INSERTS\nUSE hospital_analytics_db;\n\n")
        
        # Branches
        f.write("-- 1. Hospital Branches\n")
        for b in data["branches"]:
            f.write(f"INSERT INTO hospital_branches VALUES ({b['branch_id']}, '{b['branch_name']}', '{b['city']}', '{b['state']}', '{b['zip_code']}', '{b['phone']}', {b['total_beds']}, {b['established_year']}, NOW());\n")
        
        # Departments
        f.write("\n-- 2. Departments\n")
        for d in data["departments"]:
            f.write(f"INSERT INTO departments VALUES ({d['department_id']}, '{d['department_name']}', '{d['department_head']}', {d['floor_number']}, {d['annual_budget']}, NOW());\n")
        
        # Doctors
        f.write("\n-- 3. Doctors\n")
        for doc in data["doctors"]:
            f.write(f"INSERT INTO doctors VALUES ({doc['doctor_id']}, '{doc['first_name']}', '{doc['last_name']}', '{doc['gender']}', '{doc['email']}', '{doc['phone']}', '{doc['specialization']}', {doc['department_id']}, {doc['branch_id']}, {doc['experience_years']}, {doc['consultation_fee']}, '{doc['qualification']}', '{doc['joining_date']}', NOW());\n")
        
        # Patients
        f.write("\n-- 4. Patients\n")
        for p in data["patients"]:
            f.write(f"INSERT INTO patients VALUES ({p['patient_id']}, '{p['first_name']}', '{p['last_name']}', '{p['gender']}', '{p['dob']}', '{p['phone']}', '{p['email']}', '{p['address']}', '{p['city']}', '{p['state']}', '{p['blood_group']}', '{p['emergency_contact']}', '{p['registration_date']}', NOW());\n")

        # Disease Categories
        f.write("\n-- 5. Disease Categories\n")
        for dc in data["disease_categories"]:
            f.write(f"INSERT INTO disease_categories VALUES ({dc['disease_id']}, '{dc['disease_name']}', '{dc['category']}', '{dc['severity_level']}', '{dc['icd_code']}', '{dc['description']}', NOW());\n")

        # Medicines
        f.write("\n-- 6. Medicines\n")
        for m in data["medicines"]:
            f.write(f"INSERT INTO medicines VALUES ({m['medicine_id']}, '{m['medicine_name']}', '{m['manufacturer']}', {m['unit_cost']}, {m['stock_quantity']}, '{m['category']}', NOW());\n")

    print("[OK] Successfully generated sql/02_data_inserts.sql")
