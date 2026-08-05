# Installation & Deployment Guide

## 📌 Prerequisites

Before running the **Hospital Data Analytics Dashboard System**, ensure you have the following installed on your machine:

- **Python 3.9+** ([Download Python](https://www.python.org/downloads/))
- **MySQL Server 8.0+** ([Download MySQL](https://dev.mysql.com/downloads/installer/)) or Docker alternative
- **Git** ([Download Git](https://git-scm.com/))
- Modern Web Browser (Chrome, Firefox, Edge, Safari)

---

## 🛠️ Step-by-Step Installation

### Step 1: Clone the Repository
Open PowerShell / Terminal and run:
```bash
git clone https://github.com/your-username/Hospital-Data-Analytics-Dashboard.git
cd Hospital-Data-Analytics-Dashboard
```

---

### Step 2: Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
```
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

---

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Step 4: Database Setup (MySQL)

1. Open your MySQL client (MySQL Workbench, TablePlus, or command line) and run:
   ```sql
   CREATE DATABASE hospital_analytics_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Execute the DDL Schema Script:
   ```bash
   mysql -u root -p hospital_analytics_db < sql/01_schema_ddl.sql
   ```

3. (Optional) Populate initial data via inserts or Python generator:
   ```bash
   python scripts/generate_data.py
   mysql -u root -p hospital_analytics_db < sql/02_data_inserts.sql
   ```

4. Execute Advanced Analytical Queries & Views:
   ```bash
   mysql -u root -p hospital_analytics_db < sql/03_advanced_sql_queries.sql
   ```

---

### Step 5: Run the Web Dashboard REST API Server

Start the Flask server:
```bash
python server.py
```

Expected terminal output:
```text
[START] Starting Hospital Analytics REST API Server on port 8080...
 * Serving Flask app 'server'
 * Running on http://127.0.0.1:8080
```

---

### Step 6: Access the Dashboard

Open your browser and navigate to:
👉 **`http://localhost:8080`**

From here you can:
- Explore all 9 analytics modules (Executive Overview, Doctor Performance, Financials, AI Simulator, etc.).
- Go to **📂 Dataset Manager** to upload your own custom `patients.csv`, `doctors.csv`, `appointments.csv`, `treatments.csv`, and `billing.csv` files.
