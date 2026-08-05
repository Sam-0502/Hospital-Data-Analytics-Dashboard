import os
import json
import re
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, send_file

app = Flask(__name__, static_folder="public", static_url_path="")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB max upload size
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SAMPLES_DIR = os.path.join(DATA_DIR, "samples")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
HISTORY_FILE = os.path.join(DATA_DIR, "upload_history.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SAMPLES_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Required column schemas for 5 tables
REQUIRED_COLUMNS = {
    "patients": ["patient_id", "first_name", "last_name", "gender", "date_of_birth", "registration_date"],
    "doctors": ["doctor_id", "first_name", "last_name", "specialization", "years_experience", "hospital_branch"],
    "appointments": ["appointment_id", "patient_id", "doctor_id", "appointment_date", "appointment_time", "status"],
    "treatments": ["treatment_id", "appointment_id", "treatment_type", "cost", "treatment_date"],
    "billing": ["bill_id", "patient_id", "treatment_id", "bill_date", "amount", "payment_method", "payment_status"]
}

PRIMARY_KEYS = {
    "patients": "patient_id",
    "doctors": "doctor_id",
    "appointments": "appointment_id",
    "treatments": "treatment_id",
    "billing": "bill_id"
}

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

def log_upload_history(table_name, filename, rows, status, message):
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except Exception:
            history = []
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "table": table_name,
        "filename": filename,
        "rows": rows,
        "status": status,
        "message": message
    }
    history.insert(0, entry)
    history = history[:50] # Keep last 50 entries
    
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

def validate_and_process_df(table_name, df):
    report = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "preview": df.head(10).fillna("").to_dict(orient="records")
    }

    req_cols = REQUIRED_COLUMNS.get(table_name, [])
    pk_col = PRIMARY_KEYS.get(table_name, None)

    # 1. Check required columns
    missing_cols = [c for c in req_cols if c not in df.columns]
    if missing_cols:
        report["valid"] = False
        report["errors"].append(f"Missing required column(s): {', '.join(missing_cols)}")

    # 2. Check Primary Key uniqueness & empty IDs
    if pk_col and pk_col in df.columns:
        empty_pks = df[pk_col].isnull().sum() + (df[pk_col] == "").sum()
        if empty_pks > 0:
            report["valid"] = False
            report["errors"].append(f"Found {empty_pks} rows with empty/missing Primary Key ({pk_col})")

        dup_pks = df[pk_col].duplicated().sum()
        if dup_pks > 0:
            report["valid"] = False
            report["errors"].append(f"Found {dup_pks} duplicate Primary Key value(s) in column '{pk_col}'")

    # 3. Numeric & Date formatting checks
    if table_name == "billing" and "amount" in df.columns:
        non_numeric = pd.to_numeric(df["amount"], errors='coerce').isnull().sum()
        if non_numeric > 0:
            report["warnings"].append(f"{non_numeric} rows have non-numeric or empty values in 'amount' column.")
    
    if table_name == "treatments" and "cost" in df.columns:
        non_numeric = pd.to_numeric(df["cost"], errors='coerce').isnull().sum()
        if non_numeric > 0:
            report["warnings"].append(f"{non_numeric} rows have non-numeric values in 'cost' column.")

    return report

def rebuild_master_json_and_sql():
    tables = ["patients", "doctors", "appointments", "treatments", "billing"]
    master_data = {}

    for t in tables:
        csv_path = os.path.join(DATA_DIR, f"{t}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path).fillna("")
            master_data[t] = df.to_dict(orient="records")
        else:
            master_data[t] = []

    # Write data/hospital_data.json
    json_path = os.path.join(DATA_DIR, "hospital_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=2)

    # Generate sql/02_data_inserts.sql
    sql_path = os.path.join(os.path.dirname(__file__), "sql", "02_data_inserts.sql")
    os.makedirs(os.path.dirname(sql_path), exist_ok=True)
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("-- HOSPITAL DATA ANALYTICS INSERTS\nUSE hospital_analytics_db;\n\n")

        for p in master_data.get("patients", []):
            fn = str(p.get('first_name', '')).replace("'", "''")
            ln = str(p.get('last_name', '')).replace("'", "''")
            addr = str(p.get('address', '')).replace("'", "''")
            prov = str(p.get('insurance_provider', '')).replace("'", "''")
            f.write(f"INSERT INTO patients (patient_id, first_name, last_name, gender, date_of_birth, contact_number, address, registration_date, insurance_provider, insurance_number, email) VALUES ('{p.get('patient_id')}', '{fn}', '{ln}', '{p.get('gender')}', '{p.get('date_of_birth')}', '{p.get('contact_number')}', '{addr}', '{p.get('registration_date')}', '{prov}', '{p.get('insurance_number')}', '{p.get('email')}');\n")

        for d in master_data.get("doctors", []):
            fn = str(d.get('first_name', '')).replace("'", "''")
            ln = str(d.get('last_name', '')).replace("'", "''")
            spec = str(d.get('specialization', '')).replace("'", "''")
            branch = str(d.get('hospital_branch', '')).replace("'", "''")
            f.write(f"INSERT INTO doctors (doctor_id, first_name, last_name, specialization, phone_number, years_experience, hospital_branch, email) VALUES ('{d.get('doctor_id')}', '{fn}', '{ln}', '{spec}', '{d.get('phone_number')}', {d.get('years_experience', 0)}, '{branch}', '{d.get('email')}');\n")

        for a in master_data.get("appointments", []):
            reason = str(a.get('reason_for_visit', '')).replace("'", "''")
            f.write(f"INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit, status) VALUES ('{a.get('appointment_id')}', '{a.get('patient_id')}', '{a.get('doctor_id')}', '{a.get('appointment_date')}', '{a.get('appointment_time')}', '{reason}', '{a.get('status')}');\n")

        for t in master_data.get("treatments", []):
            ttype = str(t.get('treatment_type', '')).replace("'", "''")
            desc = str(t.get('description', '')).replace("'", "''")
            f.write(f"INSERT INTO treatments (treatment_id, appointment_id, treatment_type, description, cost, treatment_date) VALUES ('{t.get('treatment_id')}', '{t.get('appointment_id')}', '{ttype}', '{desc}', {t.get('cost', 0)}, '{t.get('treatment_date')}');\n")

        for b in master_data.get("billing", []):
            f.write(f"INSERT INTO billing (bill_id, patient_id, treatment_id, bill_date, amount, payment_method, payment_status) VALUES ('{b.get('bill_id')}', '{b.get('patient_id')}', '{b.get('treatment_id')}', '{b.get('bill_date')}', {b.get('amount', 0)}, '{b.get('payment_method')}', '{b.get('payment_status')}');\n")

    return master_data

# STATIC WEB ROUTES
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    if os.path.exists(os.path.join('public', path)):
        return send_from_directory('public', path)
    if os.path.exists(os.path.join('data', path)):
        return send_from_directory('data', path)
    return send_from_directory('public', 'index.html')

# API ENDPOINTS
@app.route('/api/data', methods=['GET'])
def get_dataset():
    json_path = os.path.join(DATA_DIR, "hospital_data.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"error": "Dataset not found"}), 404

@app.route('/api/status', methods=['GET'])
def get_status():
    tables = ["patients", "doctors", "appointments", "treatments", "billing"]
    status = {}

    for t in tables:
        csv_path = os.path.join(DATA_DIR, f"{t}.csv")
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                status[t] = {
                    "uploaded": True,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "missing_values": int(df.isnull().sum().sum()),
                    "duplicates": int(df.duplicated().sum()),
                    "last_modified": os.path.getmtime(csv_path)
                }
            except Exception as e:
                status[t] = {"uploaded": False, "error": str(e), "rows": 0, "columns": 0}
        else:
            status[t] = {"uploaded": False, "rows": 0, "columns": 0}

    return jsonify(status)

@app.route('/api/history', methods=['GET'])
def get_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
            return jsonify(history)
        except Exception:
            pass
    return jsonify([])

@app.route('/api/upload/<table_name>', methods=['POST'])
def upload_single_file(table_name):
    table_name = table_name.lower().replace('.csv', '').replace('.xlsx', '')
    if table_name not in REQUIRED_COLUMNS:
        return jsonify({"valid": False, "errors": [f"Invalid table name '{table_name}'. Supported tables: patients, doctors, appointments, treatments, billing."]}), 400

    if 'file' not in request.files:
        return jsonify({"valid": False, "errors": ["No file uploaded"]}), 400

    file = request.files['file']
    filename = sanitize_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ['.csv', '.xlsx']:
        return jsonify({"valid": False, "errors": [f"Unsupported file format '{ext}'. Only CSV (.csv) and Excel (.xlsx) files are allowed."]}), 400

    try:
        if ext == '.csv':
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        report = validate_and_process_df(table_name, df)

        if report["valid"]:
            target_csv = os.path.join(DATA_DIR, f"{table_name}.csv")
            df.to_csv(target_csv, index=False)
            rebuild_master_json_and_sql()
            report["message"] = f"Dataset '{table_name}.csv' successfully uploaded and imported ({len(df)} rows)."
            log_upload_history(table_name, filename, len(df), "Success", report["message"])
        else:
            log_upload_history(table_name, filename, len(df), "Failed", "; ".join(report["errors"]))

        return jsonify(report)

    except Exception as e:
        err_msg = f"File parsing error: {str(e)}"
        log_upload_history(table_name, filename, 0, "Failed", err_msg)
        return jsonify({"valid": False, "errors": [err_msg]}), 500

@app.route('/api/upload/all', methods=['POST'])
def upload_all_files():
    results = {}
    total_imported = 0

    for key in request.files:
        file = request.files[key]
        filename = sanitize_filename(file.filename)
        ext = os.path.splitext(filename)[1].lower()

        table_name = key.lower()
        if table_name not in REQUIRED_COLUMNS:
            base = os.path.splitext(filename)[0].lower()
            for t in REQUIRED_COLUMNS.keys():
                if t in base:
                    table_name = t
                    break

        if table_name not in REQUIRED_COLUMNS:
            continue

        if ext in ['.csv', '.xlsx']:
            try:
                df = pd.read_csv(file) if ext == '.csv' else pd.read_excel(file)
                report = validate_and_process_df(table_name, df)
                if report["valid"]:
                    df.to_csv(os.path.join(DATA_DIR, f"{table_name}.csv"), index=False)
                    total_imported += len(df)
                    log_upload_history(table_name, filename, len(df), "Success", f"Batch uploaded ({len(df)} rows)")
                else:
                    log_upload_history(table_name, filename, len(df), "Failed", "; ".join(report["errors"]))
                results[table_name] = report
            except Exception as e:
                results[table_name] = {"valid": False, "errors": [str(e)]}

    rebuild_master_json_and_sql()
    return jsonify({
        "status": "success",
        "message": f"Batch upload processed successfully. Imported records into {len(results)} tables.",
        "results": results
    })

@app.route('/api/delete/<table_name>', methods=['DELETE', 'POST'])
def delete_single_dataset(table_name):
    table_name = table_name.lower()
    target_csv = os.path.join(DATA_DIR, f"{table_name}.csv")
    if os.path.exists(target_csv):
        os.remove(target_csv)
        rebuild_master_json_and_sql()
        log_upload_history(table_name, f"{table_name}.csv", 0, "Cleared", "Dataset cleared by user")
        return jsonify({"status": "success", "message": f"Dataset '{table_name}' cleared successfully."})
    return jsonify({"status": "error", "message": f"Dataset '{table_name}' does not exist."}), 404

@app.route('/api/import', methods=['POST'])
def import_and_rebuild():
    data = rebuild_master_json_and_sql()
    return jsonify({
        "status": "success",
        "message": "Dataset successfully imported into database and dashboard models refreshed.",
        "counts": {k: len(v) for k, v in data.items()}
    })

@app.route('/api/reset', methods=['POST'])
def reset_dataset():
    tables = ["patients", "doctors", "appointments", "treatments", "billing"]
    for t in tables:
        target_csv = os.path.join(DATA_DIR, f"{t}.csv")
        if os.path.exists(target_csv):
            os.remove(target_csv)
    
    try:
        import scripts.etl_import_csv as etl
        etl.run_etl()
    except Exception:
        rebuild_master_json_and_sql()

    log_upload_history("all", "system_reset", 0, "Reset", "Dataset reset to initial state")
    return jsonify({"status": "success", "message": "Datasets reset to original baseline data."})

@app.route('/api/sample/<table_name>', methods=['GET'])
def download_sample(table_name):
    table_name = table_name.lower().replace('.csv', '').replace('.xlsx', '')
    filename = f"sample_{table_name}.csv"
    filepath = os.path.join(SAMPLES_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({"error": "Sample file not found"}), 404

if __name__ == '__main__':
    print("[START] Starting Hospital Analytics REST API Server on port 8080...")
    app.run(host='0.0.0.0', port=8080, debug=True)
