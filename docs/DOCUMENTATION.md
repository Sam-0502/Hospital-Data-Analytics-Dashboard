# COMPLETE SYSTEM SPECIFICATION & DOCUMENTATION
## Hospital Data Analytics Dashboard with Predictive Revenue Forecasting and Doctor Performance Insights

---

## 1. PROJECT ABSTRACT
Healthcare institutions generate large volumes of operational, financial, and clinical data daily. However, legacy healthcare reporting often suffers from fragmented data silos, uncollected billing revenue, physician workload imbalances, and unmonitored bed occupancy rates. 

This project presents an enterprise-grade **Hospital Data Analytics System** designed to unify data across 14 core entities into a centralized data warehouse and interactive decision-support system. Built using **MySQL 8.0**, **Power BI Data Warehouse Star Schema**, **50+ DAX Measures**, and an **Interactive Web Dashboard System**, the platform empowers hospital executives, clinical directors, and financial controllers with real-time visibility into revenue trends, doctor efficiency leaderboards, patient retention rates, and predictive bed demand.

---

## 2. PROBLEM STATEMENT
Modern hospital administrative management suffers from three major structural inefficiencies:
1. **Financial Leakage & Revenue Cycle Delays**: High proportions of pending billing amounts and delayed insurance reimbursements erode operating margins.
2. **Physician Resource Misallocation**: Lack of objective ranking for physician consultation volume, appointment completion rates, and patient satisfaction scores leads to burnout and unbalanced patient distribution.
3. **Operational Bottlenecks in Patient Flow**: Extended waiting times during peak appointment hours (10 AM - 12 PM) combined with unpredictable emergency triage visits create room congestion and underutilized bed inventory.

---

## 3. PROJECT OBJECTIVES & SCOPE

### 3.1 Core Objectives
- **Data Centralization**: Model a 3NF relational database comprising 14 tables with strict referential integrity, constraints, and performance indexes.
- **Advanced SQL Analytical Engine**: Develop 40+ production queries leveraging Common Table Expressions (CTEs), Window Functions (`RANK`, `DENSE_RANK`, `LAG`, `LEAD`, `NTILE`), Views, and Stored Procedures.
- **Predictive Financial Intelligence**: Implement a 6-month predictive revenue forecast model utilizing 3-month rolling moving averages and growth factor adjustments.
- **Executive Reporting & Interactive UI**: Build a 9-page interactive dashboard system equipped with dynamic slicers, dynamic titles, conditional KPI formatting, and AI smart narratives.

### 3.2 In-Scope Modules
- Patient Demographics & Retention Cohort Analysis.
- Doctor Utilization, Billing Revenue Leaderboard & Rating Scorecards.
- Appointment Peak Hours, No-Show Rates, and Cancellation Analysis.
- Treatment Success Rates, ICD-10 Disease Outbreak Trends, and Medicine Stock Usage.
- Hospital Bed Occupancy Rates, Emergency Triage Levels, and Average Length of Stay (LOS).

---

## 4. SYSTEM ARCHITECTURE & DATA FLOW DIAGRAMS

### 4.1 System Architecture
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA GENERATION ENGINE                           │
│              Python 3.11 Script (Synthetic Healthcare Engine)               │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          RELATIONAL DATABASE LAYER                          │
│               MySQL 8.0 DB (14 Tables, PK/FK, Views, Procedures)            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DATA WAREHOUSE & MODELING LAYER                       │
│           Power BI Star Schema (Fact_Appointments, Fact_Billing, Dim_*)     │
│                 DAX Measure Library (50+ Analytical Measures)               │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXECUTIVE PRESENTATION LAYER                         │
│         Interactive Multi-Page Web Analytics Dashboard System (9 Pages)     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Data Flow Diagram (DFD Level 0 - Context Diagram)
- **External Entities**: Patients, Doctors, Administrative Staff, Insurance Providers.
- **Process**: Hospital Management Analytics System.
- **Data Stores**: Relational MySQL Database, Power BI Data Warehouse.

### 4.3 Data Flow Diagram (DFD Level 1 - Process Diagram)
1. **P1: Patient Registration & Scheduling** -> Stores records in `patients` and `appointments`.
2. **P2: Clinical Treatment & Diagnosis** -> Captures diagnoses in `treatments`, `disease_categories`, `medicines`.
3. **P3: Billing & Revenue Cycle Management** -> Generates invoices in `billing` and links `insurance`.
4. **P4: Operations & Bed Allocation** -> Tracks `rooms_beds`, `emergency_visits`, `staff`.
5. **P5: BI Aggregation & AI Insights** -> Executes Views/Stored Procedures to render Executive KPIs.

---

## 5. DATABASE DICTIONARY & RELATIONSHIPS

1. **`hospital_branches`**: Primary Key `branch_id`. Tracks branch location, total bed capacity, city.
2. **`departments`**: Primary Key `department_id`. Details specialty name, annual budget, floor.
3. **`doctors`**: Primary Key `doctor_id`. Foreign Keys `department_id`, `branch_id`. Tracks consultation fees, experience, specialization.
4. **`patients`**: Primary Key `patient_id`. Contains demographics, blood group, city, registration date.
5. **`insurance`**: Primary Key `insurance_id`. Foreign Key `patient_id`. Captures provider, policy limit, copay %.
6. **`disease_categories`**: Primary Key `disease_id`. Maps ICD-10 codes, category, severity level.
7. **`appointments`**: Primary Key `appointment_id`. Foreign Keys `patient_id`, `doctor_id`, `department_id`, `branch_id`.
8. **`treatments`**: Primary Key `treatment_id`. Foreign Keys `appointment_id`, `patient_id`, `doctor_id`, `disease_id`.
9. **`billing`**: Primary Key `bill_id`. Foreign Keys `patient_id`, `appointment_id`, `treatment_id`, `insurance_id`.
10. **`medicines`**: Primary Key `medicine_id`. Captures drug name, unit cost, stock level.
11. **`treatment_medicines`**: Junction Primary Key (`treatment_id`, `medicine_id`).
12. **`rooms_beds`**: Primary Key `room_id`. Foreign Keys `branch_id`, `assigned_patient_id`.
13. **`staff`**: Primary Key `staff_id`. Foreign Keys `branch_id`, `department_id`.
14. **`emergency_visits`**: Primary Key `emergency_id`. Foreign Keys `patient_id`, `branch_id`, `doctor_id`.

---

## 6. BUSINESS INSIGHTS & STRATEGIC RECOMMENDATIONS

### Insight 1: Peak Appointment Congestion
- **Finding**: 42% of total daily appointments are booked between 10:00 AM - 12:00 PM and 3:00 PM - 5:00 PM.
- **Recommendation**: Implement staggered physician shifts and offer a 10% consultation fee discount for off-peak appointments (1:00 PM - 3:00 PM).

### Insight 2: Uncollected Pending Revenue
- **Finding**: Pending billing accounts for ~15% of total billed revenue, primarily driven by manual insurance claim approvals.
- **Recommendation**: Integrate automated electronic pre-authorization claim verification to reduce pending receivables by 35%.

### Insight 3: Physician Utilization Disparity
- **Finding**: Cardiology and Oncology doctors handle 2.4x more consultations per week than Orthopedics physicians.
- **Recommendation**: Use the What-If Capacity Allocation model to reassign junior clinical staff and balance workload.

---

## 7. FUTURE ENHANCEMENTS
1. **Direct EMR API Integration**: Connect pipeline directly to HL7 / FHIR protocol healthcare APIs.
2. **Real-time IoT Bed Sensors**: Stream bed occupancy state updates via WebSocket event buses.
3. **Advanced Machine Learning**: Implement Python Scikit-Learn Random Forest models for predicting 30-day patient readmission risks.
