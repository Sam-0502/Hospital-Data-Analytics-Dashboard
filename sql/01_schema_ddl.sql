-- =============================================================================
-- HOSPITAL DATA ANALYTICS SYSTEM - ENTERPRISE MYSQL SCHEMA (5 CSV ARCHITECTURE)
-- Based strictly on uploaded dataset tables: patients, doctors, appointments, treatments, billing
-- =============================================================================

CREATE DATABASE IF NOT EXISTS hospital_analytics_db;
USE hospital_analytics_db;

DROP TABLE IF EXISTS billing;
DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;

-- -----------------------------------------------------------------------------
-- 1. PATIENTS TABLE (from patients.csv)
-- -----------------------------------------------------------------------------
CREATE TABLE patients (
    patient_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    contact_number VARCHAR(25),
    address VARCHAR(255),
    registration_date DATE NOT NULL,
    insurance_provider VARCHAR(100),
    insurance_number VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 2. DOCTORS TABLE (from doctors.csv)
-- -----------------------------------------------------------------------------
CREATE TABLE doctors (
    doctor_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone_number VARCHAR(25),
    years_experience INT NOT NULL DEFAULT 0,
    hospital_branch VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 3. APPOINTMENTS TABLE (from appointments.csv)
-- -----------------------------------------------------------------------------
CREATE TABLE appointments (
    appointment_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    doctor_id VARCHAR(20) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    reason_for_visit VARCHAR(255),
    status VARCHAR(50) NOT NULL DEFAULT 'Completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_app_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    CONSTRAINT fk_app_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 4. TREATMENTS TABLE (from treatments.csv)
-- -----------------------------------------------------------------------------
CREATE TABLE treatments (
    treatment_id VARCHAR(20) PRIMARY KEY,
    appointment_id VARCHAR(20) NOT NULL,
    treatment_type VARCHAR(100) NOT NULL,
    description TEXT,
    cost DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    treatment_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_treat_appointment FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 5. BILLING TABLE (from billing.csv)
-- -----------------------------------------------------------------------------
CREATE TABLE billing (
    bill_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    treatment_id VARCHAR(20) NOT NULL,
    bill_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'Paid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bill_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    CONSTRAINT fk_bill_treatment FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================================================
-- INDEXES FOR QUERY OPTIMIZATION
-- =============================================================================
CREATE INDEX idx_patients_reg ON patients(registration_date);
CREATE INDEX idx_doctors_dept ON doctors(specialization);
CREATE INDEX idx_doctors_branch ON doctors(hospital_branch);
CREATE INDEX idx_app_date ON appointments(appointment_date);
CREATE INDEX idx_app_status ON appointments(status);
CREATE INDEX idx_treat_type ON treatments(treatment_type);
CREATE INDEX idx_bill_date ON billing(bill_date);
CREATE INDEX idx_bill_status ON billing(payment_status);

-- =============================================================================
-- REPORTING VIEWS FOR POWER BI & EXECUTIVE DASHBOARD
-- =============================================================================

CREATE OR REPLACE VIEW vw_executive_analytics_master AS
SELECT 
    b.bill_id,
    b.bill_date,
    b.amount AS bill_amount,
    b.payment_method,
    b.payment_status,
    t.treatment_id,
    t.treatment_type,
    t.description AS treatment_description,
    t.cost AS treatment_cost,
    app.appointment_id,
    app.appointment_date,
    app.appointment_time,
    app.reason_for_visit,
    app.status AS appointment_status,
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.gender AS patient_gender,
    p.date_of_birth AS patient_dob,
    TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE()) AS patient_age,
    p.insurance_provider,
    doc.doctor_id,
    CONCAT(doc.first_name, ' ', doc.last_name) AS doctor_name,
    doc.specialization,
    doc.years_experience,
    doc.hospital_branch
FROM billing b
INNER JOIN treatments t ON b.treatment_id = t.treatment_id
INNER JOIN appointments app ON t.appointment_id = app.appointment_id
INNER JOIN patients p ON b.patient_id = p.patient_id
INNER JOIN doctors doc ON app.doctor_id = doc.doctor_id;
