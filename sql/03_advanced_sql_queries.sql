-- =============================================================================
-- HOSPITAL DATA ANALYTICS SYSTEM - ADVANCED SQL QUERIES (5 CSV SCHEMA)
-- Target: MySQL 8.0+ / PostgreSQL
-- Based on uploaded CSV tables: patients, doctors, appointments, treatments, billing
-- =============================================================================

USE hospital_analytics_db;

-- =============================================================================
-- SECTION 1: EXECUTIVE KPIs & AGGREGATIONS
-- =============================================================================

-- Query 1.1: Core Executive Metrics Summary
SELECT 
    (SELECT COUNT(*) FROM patients) AS total_patients,
    (SELECT COUNT(*) FROM doctors) AS total_doctors,
    (SELECT COUNT(*) FROM appointments) AS total_appointments,
    (SELECT SUM(amount) FROM billing) AS total_revenue,
    (SELECT SUM(amount) FROM billing WHERE payment_status = 'Pending') AS total_pending_revenue,
    (SELECT SUM(amount) FROM billing WHERE payment_status IN ('Paid', 'Completed')) AS total_paid_revenue,
    (SELECT AVG(cost) FROM treatments) AS avg_treatment_cost,
    (SELECT COUNT(*) FROM appointments WHERE status = 'Cancelled') AS total_cancelled_appointments,
    (SELECT COUNT(*) FROM appointments WHERE status = 'No-show') AS total_no_show_appointments;

-- Query 1.2: Revenue & Patient Volume by Doctor Specialization (HAVING Clause)
SELECT 
    doc.specialization,
    COUNT(DISTINCT doc.doctor_id) AS doctor_count,
    COUNT(DISTINCT app.appointment_id) AS total_appointments,
    COALESCE(SUM(b.amount), 0) AS total_revenue_generated,
    ROUND(AVG(b.amount), 2) AS avg_revenue_per_bill
FROM doctors doc
LEFT JOIN appointments app ON doc.doctor_id = app.doctor_id
LEFT JOIN treatments t ON app.appointment_id = t.appointment_id
LEFT JOIN billing b ON t.treatment_id = b.treatment_id
GROUP BY doc.specialization
HAVING total_revenue_generated > 5000
ORDER BY total_revenue_generated DESC;

-- =============================================================================
-- SECTION 2: ADVANCED WINDOW FUNCTIONS & RANKING
-- =============================================================================

-- Query 2.1: Doctor Performance Leaderboard using DENSE_RANK() & NTILE()
WITH DoctorPerformanceCTE AS (
    SELECT 
        doc.doctor_id,
        CONCAT(doc.first_name, ' ', doc.last_name) AS doctor_name,
        doc.specialization,
        doc.hospital_branch,
        doc.years_experience,
        COUNT(DISTINCT app.appointment_id) AS appointments_handled,
        COALESCE(SUM(b.amount), 0) AS total_revenue
    FROM doctors doc
    LEFT JOIN appointments app ON doc.doctor_id = app.doctor_id
    LEFT JOIN treatments t ON app.appointment_id = t.appointment_id
    LEFT JOIN billing b ON t.treatment_id = b.treatment_id
    GROUP BY doc.doctor_id, doctor_name, doc.specialization, doc.hospital_branch, doc.years_experience
)
SELECT 
    doctor_name,
    specialization,
    hospital_branch,
    years_experience,
    appointments_handled,
    total_revenue,
    DENSE_RANK() OVER (PARTITION BY specialization ORDER BY total_revenue DESC) AS spec_revenue_rank,
    RANK() OVER (ORDER BY total_revenue DESC) AS overall_hospital_rank,
    NTILE(4) OVER (ORDER BY total_revenue DESC) AS performance_quartile
FROM DoctorPerformanceCTE
ORDER BY overall_hospital_rank ASC;

-- Query 2.2: Month-over-Month Revenue Growth using LAG() Window Function
WITH MonthlyRevenueCTE AS (
    SELECT 
        DATE_FORMAT(bill_date, '%Y-%m') AS billing_month,
        SUM(amount) AS monthly_revenue,
        COUNT(bill_id) AS bill_count
    FROM billing
    GROUP BY DATE_FORMAT(bill_date, '%Y-%m')
)
SELECT 
    billing_month,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY billing_month) AS prev_month_revenue,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY billing_month)) / 
        NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY billing_month), 0)) * 100, 2
    ) AS mom_growth_pct,
    AVG(monthly_revenue) OVER (ORDER BY billing_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS 3_month_moving_avg
FROM MonthlyRevenueCTE
ORDER BY billing_month ASC;

-- =============================================================================
-- SECTION 3: PATIENT DEMOGRAPHICS & CLINICAL INSIGHTS
-- =============================================================================

-- Query 3.1: Patient Age Group & Insurance Coverage Breakdown
WITH PatientAgeCTE AS (
    SELECT 
        patient_id,
        gender,
        insurance_provider,
        TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) AS age,
        CASE 
            WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) < 18 THEN 'Pediatric (<18)'
            WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 18 AND 35 THEN 'Young Adult (18-35)'
            WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 36 AND 60 THEN 'Middle Adult (36-60)'
            ELSE 'Senior Citizen (60+)'
        END AS age_group
    FROM patients
)
SELECT 
    age_group,
    gender,
    insurance_provider,
    COUNT(patient_id) AS patient_count
FROM PatientAgeCTE
GROUP BY age_group, gender, insurance_provider
ORDER BY patient_count DESC;

-- Query 3.2: Peak Appointment Hours Analysis
SELECT 
    HOUR(appointment_time) AS appointment_hour,
    COUNT(*) AS total_booked_appointments,
    SUM(CASE WHEN status = 'Scheduled' THEN 1 ELSE 0 END) AS scheduled_count,
    SUM(CASE WHEN status = 'No-show' THEN 1 ELSE 0 END) AS no_show_count,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_count
FROM appointments
GROUP BY HOUR(appointment_time)
ORDER BY appointment_hour ASC;

-- =============================================================================
-- SECTION 4: VIEWS & STORED PROCEDURES
-- =============================================================================

-- View: vw_doctor_scorecard
CREATE OR REPLACE VIEW vw_doctor_scorecard AS
SELECT 
    doc.doctor_id,
    CONCAT(doc.first_name, ' ', doc.last_name) AS doctor_name,
    doc.specialization,
    doc.hospital_branch,
    COUNT(DISTINCT app.appointment_id) AS total_appointments,
    COALESCE(SUM(b.amount), 0) AS total_revenue_generated
FROM doctors doc
LEFT JOIN appointments app ON doc.doctor_id = app.doctor_id
LEFT JOIN treatments t ON app.appointment_id = t.appointment_id
LEFT JOIN billing b ON t.treatment_id = b.treatment_id
GROUP BY doc.doctor_id, doctor_name, doc.specialization, doc.hospital_branch;

DELIMITER //

-- Procedure: Predict Revenue Forecast
CREATE PROCEDURE sp_predict_monthly_revenue_forecast()
BEGIN
    WITH MonthlyData AS (
        SELECT 
            DATE_FORMAT(bill_date, '%Y-%m') AS billing_month,
            SUM(amount) AS actual_revenue
        FROM billing
        GROUP BY DATE_FORMAT(bill_date, '%Y-%m')
    )
    SELECT 
        billing_month,
        actual_revenue,
        AVG(actual_revenue) OVER (ORDER BY billing_month ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) AS baseline_forecast,
        ROUND(AVG(actual_revenue) OVER (ORDER BY billing_month ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) * 1.05, 2) AS optimistic_forecast
    FROM MonthlyData;
END //

DELIMITER ;
