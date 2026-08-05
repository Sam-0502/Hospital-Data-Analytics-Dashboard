# Flask REST API Documentation

## 🔌 API Endpoints Specification

Base URL: `http://localhost:8080`

---

### 1. `GET /api/data`
- **Description**: Returns the complete aggregated dataset (patients, doctors, appointments, treatments, billing) for web front-end chart rendering.
- **Response Format**: `JSON`
- **Sample Response**:
  ```json
  {
    "patients": [{ "patient_id": "PAT-001", "first_name": "John", "last_name": "Doe", ... }],
    "doctors": [{ "doctor_id": "DOC-001", "first_name": "Sarah", "specialization": "Cardiology", ... }],
    "appointments": [...],
    "treatments": [...],
    "billing": [...]
  }
  ```

---

### 2. `GET /api/status`
- **Description**: Returns the ingestion and upload status for all 5 dataset tables.
- **Response Format**: `JSON`
- **Sample Response**:
  ```json
  {
    "patients": { "uploaded": true, "rows": 50, "columns": 8, "missing_values": 0, "duplicates": 0 },
    "doctors": { "uploaded": true, "rows": 10, "columns": 8, "missing_values": 0, "duplicates": 0 },
    "appointments": { "uploaded": true, "rows": 200, "columns": 7, "missing_values": 0, "duplicates": 0 },
    "treatments": { "uploaded": true, "rows": 200, "columns": 6, "missing_values": 0, "duplicates": 0 },
    "billing": { "uploaded": true, "rows": 200, "columns": 7, "missing_values": 0, "duplicates": 0 }
  }
  ```

---

### 3. `POST /api/upload/<table_name>`
- **Description**: Uploads and validates an individual dataset file (`.csv` or `.xlsx`).
- **Path Parameters**: `table_name` = `patients`, `doctors`, `appointments`, `treatments`, or `billing`.
- **Payload**: `multipart/form-data` with `file` key.
- **Validation Rules**:
  - Max file size: **25 MB**.
  - Enforces required primary key columns.
  - Checks for duplicate primary keys and empty ID rows.
  - Checks for numeric formatting on `cost` and `amount` fields.
- **Sample Response**:
  ```json
  {
    "valid": true,
    "rows": 50,
    "columns": 8,
    "missing_values": 0,
    "duplicate_rows": 0,
    "errors": [],
    "warnings": [],
    "message": "Dataset 'patients.csv' successfully uploaded and imported (50 rows)."
  }
  ```

---

### 4. `POST /api/upload/all`
- **Description**: Batch uploads multiple dataset files at once.
- **Payload**: `multipart/form-data` with multiple files.

---

### 5. `DELETE /api/delete/<table_name>`
- **Description**: Clears the specified dataset file and rebuilds models.

---

### 6. `POST /api/reset`
- **Description**: Resets datasets back to initial baseline data.

---

### 7. `GET /api/sample/<table_name>`
- **Description**: Downloads template CSV template file for target table.
