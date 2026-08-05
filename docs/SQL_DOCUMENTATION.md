# Advanced SQL Queries, Views & Window Functions Documentation

## 📌 SQL Suite Overview

The project includes over **40+ enterprise analytical SQL queries** stored in `sql/03_advanced_sql_queries.sql`. These queries demonstrate mastery of:
- **INNER JOIN, LEFT JOIN, RIGHT JOIN**
- **GROUP BY & HAVING clauses**
- **Window Functions** (`RANK()`, `DENSE_RANK()`, `ROW_NUMBER()`, `SUM() OVER`, `AVG() OVER`)
- **Common Table Expressions (CTEs)**
- **SQL Reporting Views & Stored Procedures**

---

## 💡 SQL Feature Breakdown & Examples

### 1. Doctor Revenue Leaderboard using `DENSE_RANK()` Window Function
Ranks doctors by total generated revenue within each specialization and hospital branch:

```sql
WITH DoctorRevenue AS (
    SELECT 
        d.doctor_id,
        CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
        d.specialization,
        d.hospital_branch,
        COUNT(DISTINCT a.appointment_id) AS total_appointments,
        SUM(b.amount) AS total_revenue
    FROM doctors d
    INNER JOIN appointments a ON d.doctor_id = a.doctor_id
    INNER JOIN billing b ON a.patient_id = b.patient_id
    WHERE a.status = 'Completed' AND b.payment_status = 'Paid'
    GROUP BY d.doctor_id, doctor_name, d.specialization, d.hospital_branch
)
SELECT 
    doctor_name,
    specialization,
    hospital_branch,
    total_appointments,
    total_revenue,
    DENSE_RANK() OVER (PARTITION BY specialization ORDER BY total_revenue DESC) AS spec_rank,
    DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS overall_rank
FROM DoctorRevenue;
```

---

### 2. Monthly Revenue Trend & 3-Month Moving Average (Window Frame CTE)

```sql
WITH MonthlyRevenue AS (
    SELECT 
        DATE_FORMAT(bill_date, '%Y-%m') AS rev_month,
        SUM(amount) AS monthly_total
    FROM billing
    WHERE payment_status = 'Paid'
    GROUP BY rev_month
)
SELECT 
    rev_month,
    monthly_total,
    AVG(monthly_total) OVER (
        ORDER BY rev_month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3m,
    LAG(monthly_total, 1) OVER (ORDER BY rev_month) AS prev_month_total,
    ROUND(((monthly_total - LAG(monthly_total, 1) OVER (ORDER BY rev_month)) / 
           LAG(monthly_total, 1) OVER (ORDER BY rev_month)) * 100, 2) AS mom_growth_pct
FROM MonthlyRevenue;
```

---

### 3. Patient Cohort Analysis (GROUP BY & HAVING)
Identifies high-value returning patients with pending balances exceeding $1,000:

```sql
SELECT 
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.insurance_provider,
    COUNT(b.bill_id) AS total_bills,
    SUM(CASE WHEN b.payment_status = 'Pending' THEN b.amount ELSE 0 END) AS pending_balance,
    SUM(b.amount) AS lifetime_value
FROM patients p
LEFT JOIN billing b ON p.patient_id = b.patient_id
GROUP BY p.patient_id, patient_name, p.insurance_provider
HAVING pending_balance > 1000 AND total_bills >= 2
ORDER BY pending_balance DESC;
```

---

## 🗄️ SQL Views for Dashboard Reporting

1. **`view_executive_kpis`**: Pre-aggregates Total Patients, Total Doctors, Total Revenue, Pending Bills, and Completed Appointments for instantaneous dashboard loads.
2. **`view_doctor_performance`**: Combines doctor experience, patient loads, treatment counts, and revenue yield.
3. **`view_financial_monthly_summary`**: Summarizes paid, pending, and total billed revenue by year and month.
