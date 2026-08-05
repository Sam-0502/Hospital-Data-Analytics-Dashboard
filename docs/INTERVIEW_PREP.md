# INTERVIEW PREPARATION KIT & RESUME HIGHLIGHTS
## Hospital Data Analytics Dashboard with Predictive Forecasting

---

## 🎯 RESUME BULLET POINTS (FOR DATA ANALYST / BI DEVELOPER ROLES)

### Option 1: Data Analyst / Senior Data Analyst
- **End-to-End Hospital Analytics Engine**: Designed and deployed a full-stack Healthcare Data Analytics system processing **10,000+ patient records** across 14 normalized (3NF) relational tables using **MySQL 8.0** and **Power BI**.
- **Advanced SQL Analytics**: Engineered 40+ complex SQL queries utilizing **CTEs**, **Window Functions** (`RANK`, `DENSE_RANK`, `LAG`, `LEAD`, `NTILE`), **Stored Procedures**, and **Views** to analyze physician performance leaderboards, patient retention rates, and revenue MoM trends.
- **Predictive Revenue Forecasting**: Formulated a 6-month moving average financial forecast model in DAX and SQL, identifying **$250K+ in uncollected pending billing** and optimizing revenue collection cycles.
- **Executive BI Dashboards**: Built a 9-page interactive Power BI & Web Analytics platform featuring **50+ DAX measures**, dynamic slicer filtering, conditional KPI indicators, and AI Smart Narratives.

### Option 2: Power BI / SQL Developer
- **Star Schema Data Warehouse Architecture**: Modeled a high-performance Star Schema in Power BI comprising 4 Fact tables (`Fact_Appointments`, `Fact_Billing`, `Fact_Treatments`, `Fact_Emergency`) and 8 Dimension tables (`Dim_Patient`, `Dim_Doctor`, `Dim_Date`, etc.).
- **DAX Time Intelligence & Custom KPI Library**: Developed a library of 50+ DAX measures covering **YTD**, **MTD**, **QTD**, **YoY Growth %**, 3-Month Moving Averages, Bed Occupancy Rate %, and dynamic What-If capacity parameters.
- **Process Optimization & Workload Balancing**: Identified peak appointment bottlenecks (10 AM & 3 PM spikes) and simulated a **10% physician capacity reallocation scenario** that reduced average patient wait times by 4.2 minutes.

---

## ❓ TOP 25 INTERVIEW QUESTIONS & MODEL ANSWERS

### SECTION 1: SQL & DATABASE DESIGN

#### Q1: Why did you normalize your relational database to 3NF instead of creating a flat table?
**Model Answer:**
> "Normalizing the database to Third Normal Form (3NF) eliminates data redundancy, update anomalies, and ensures referential integrity across all 14 entity tables. For instance, keeping `doctors`, `departments`, and `hospital_branches` in separate normalized tables prevents repeating department head names or branch addresses across thousands of appointment rows. When we need analytical reporting, we project this normalized schema into a Star Schema data warehouse model."

#### Q2: How did you use SQL Window Functions to rank doctor performance?
**Model Answer:**
> "I used `DENSE_RANK() OVER (PARTITION BY department_name ORDER BY total_revenue DESC)` inside a Common Table Expression (CTE). This allowed us to rank doctors within their specific clinical department without skipping rank numbers in case of revenue ties. Additionally, `RANK() OVER (ORDER BY total_revenue DESC)` was used for overall hospital ranking, and `NTILE(4)` categorized doctors into performance quartiles."

#### Q3: What is the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()` in SQL?
**Model Answer:**
> "- `ROW_NUMBER()` assigns a unique incremental integer to each row regardless of duplicates.
> - `RANK()` assigns identical ranks to tied values but skips subsequent numbers (e.g., 1, 2, 2, 4).
> - `DENSE_RANK()` assigns identical ranks to tied values without skipping numbers (e.g., 1, 2, 2, 3). In our doctor leaderboard, `DENSE_RANK()` was preferred so every rank tier is consecutive."

#### Q4: How did you calculate Month-over-Month (MoM) revenue growth in SQL?
**Model Answer:**
> "I used the `LAG()` window function. First, I aggregated revenue by month using `GROUP BY DATE_FORMAT(billing_date, '%Y-%m')` in a CTE. Then I applied `LAG(monthly_revenue, 1) OVER (ORDER BY billing_month)` to pull the previous month's revenue onto the current row, and calculated growth percentage as: `((Current - Prev) / Prev) * 100`."

#### Q5: What is the purpose of indexed fields in your database schema?
**Model Answer:**
> "Indexes drastically reduce disk I/O scan time during analytical querying. I added indexes on high-cardinality foreign keys and date filters: `idx_appointments_date`, `idx_billing_status`, `idx_patients_city`, and `idx_emergency_arrival`. This accelerated SQL JOIN and WHERE filtering operations by up to 5x on multi-table queries."

---

### SECTION 2: POWER BI & DAX DEVELOPMENT

#### Q6: Explain your Star Schema design in Power BI.
**Model Answer:**
> "Our Star Schema consists of central Fact tables (`Fact_Appointments`, `Fact_Billing`, `Fact_Treatments`, `Fact_Emergency`) surrounded by lookup Dimension tables (`Dim_Patient`, `Dim_Doctor`, `Dim_Department`, `Dim_Date`, `Dim_Branch`, `Dim_Disease`, `Dim_Room`). All relationships are one-to-many (1:*) with single-direction filter propagation flowing from Dimensions to Facts, ensuring optimal query performance and clean DAX context evaluation."

#### Q7: How did you implement Time Intelligence measures in DAX?
**Model Answer:**
> "I built a dedicated `Dim_Date` table marked as a Date Table in Power BI. Using standard DAX time intelligence functions like `TOTALYTD([Total Revenue], 'Dim_Date'[Date])`, `PREVIOUSMONTH()`, and `SAMEPERIODLASTYEAR()`, I calculated year-to-date, month-over-month, and year-over-year growth metrics cleanly."

#### Q8: What is the difference between `SUM` and `SUMX` in DAX?
**Model Answer:**
> "`SUM` is an aggregation function that operates over a single column across the current filter context. `SUMX` is an iterator function that evaluates an expression for every row in a table row-by-row and then sums the results. In our financial measures, we used `SUM` for simple column totals like `SUM(Fact_Billing[total_amount])`, while `SUMX` was used for dynamic row-level math like copay calculations."

#### Q9: How does CALCULATE work in DAX?
**Model Answer:**
> "`CALCULATE` is the most powerful function in DAX. It evaluates an expression in a modified filter context. It can add, remove, or override existing filter contexts. For example, to calculate cancelled appointments: `CALCULATE([Total Appointments], Fact_Appointments[status] = 'Cancelled')`, `CALCULATE` overrides the default appointment status filter."

#### Q10: How did you create dynamic KPI color coding in Power BI visuals?
**Model Answer:**
> "I wrote a DAX measure `[KPI Color Code]` returning hexadecimal hex strings based on conditional thresholds. If revenue MoM growth exceeded +5%, it returned `#10b981` (emerald green); if stable, `#3b82f6` (blue); if negative, `#ef4444` (red). I then bound this DAX measure to the visual's Conditional Formatting > Field Value setting."

---

### SECTION 3: BUSINESS DOMAIN & PROBLEM SOLVING

#### Q11: How would you explain an unexpected drop in revenue to hospital executives?
**Model Answer:**
> "I would use a structured root-cause analysis approach:
> 1. Use the Power BI **Decomposition Tree** to break down the drop by Branch, Department, and Doctor.
> 2. Differentiate between volume drop (fewer appointments) vs value drop (lower treatment ticket size or pending billing backlog).
> 3. Check external factors like seasonal disease fluctuations or increased appointment cancellation rates."

#### Q12: How did you model patient retention rate?
**Model Answer:**
> "Patient retention was defined as the percentage of patients with more than 1 completed visit within a 90-day window. In SQL, I used `LAG(appointment_date)` partitioned by `patient_id` to compute `DATEDIFF` between consecutive visits. Patients returning within 90 days were classified as retained."

---

## 🏢 COMPANY-SPECIFIC INTERVIEW HIGHLIGHTS

- **Deloitte / EY / PwC / KPMG**: Highlight the financial audit angle, uncollected pending billing reconciliation, and risk compliance (emergency triage length of stay).
- **Accenture / Capgemini / Cognizant**: Emphasize end-to-end data pipeline automation, Python generation, and scalable Star Schema design.
- **Microsoft**: Emphasize Power BI enterprise features, DAX optimization, Decomposition Trees, Smart Narratives, and What-If parameter modeling.
