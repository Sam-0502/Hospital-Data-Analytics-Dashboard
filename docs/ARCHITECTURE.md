# System Architecture & Technical Specifications

## 📐 System Architecture Overview

```mermaid
flowchart TB
    subgraph Client["Front-End Web Client (HTML5 / Vanilla CSS / JS)"]
        UI["High-Density UI (Dark Theme)"]
        Charts["Chart.js Visualizations"]
        DSManager["📂 Dataset Manager (Drag & Drop UI)"]
    end

    subgraph Backend["Python Flask REST API (server.py)"]
        API["REST Endpoints (/api/upload, /api/data, /api/import)"]
        Validator["Validation & Parsing Engine (pandas / openpyxl)"]
        ETL["JSON & SQL Insert Generator"]
    end

    subgraph Storage["Database & File System"]
        JSONStore["data/hospital_data.json"]
        MySQLDB[("MySQL 8.0 Database (hospital_analytics_db)")]
        Uploads["data/uploads/"]
    end

    UI <--> API
    DSManager -->|CSV / XLSX Upload| API
    API --> Validator
    Validator --> ETL
    ETL --> JSONStore
    ETL --> MySQLDB
    Charts <-- Fetch Dataset JSON -- API
```

---

## 🔄 Data Flow Diagram (DFD)

```mermaid
sequenceDiagram
    autonumber
    actor User as Healthcare Manager
    participant UI as Web Dashboard UI
    participant API as Flask REST API Server
    participant Val as Validation Engine
    participant DB as MySQL Database

    User->>UI: Selects & Uploads CSV / Excel dataset
    UI->>API: POST /api/upload/<table_name> (Multipart file)
    API->>Val: Check required columns, PKs, types & dates
    Val-->>API: Validation Report (valid, errors, preview)
    alt Validation Passed
        API->>DB: Execute SQL Insert / Update
        API->>UI: Return Success & Updated JSON Data
        UI->>UI: Refresh KPIs, Charts & AI Smart Narrative
    else Validation Failed
        API->>UI: Return Error Report (Missing columns / Duplicate PKs)
        UI->>User: Display Friendly Validation Error Box
    end
```

---

## 🛠️ Technology Stack Detail

| Component | Technology | Purpose |
|---|---|---|
| **Database** | MySQL 8.0+ | Relational data persistence, Views, SPs, CTEs, Window Functions |
| **Backend API** | Python 3.9+ / Flask | REST endpoints, CSV/Excel parsing, validation engine, static file serving |
| **Data Science / ETL** | Pandas, OpenPyXL, PyMySQL | Data cleaning, data generation, batch imports |
| **Front-End UI** | HTML5, Vanilla CSS3 | Custom dark medical theme, glassmorphism, responsive single-screen layout |
| **Visualizations** | Chart.js 4.x | Line charts, Bar charts, Doughnut charts, Pie charts |
| **Icons & Typography** | FontAwesome 6, Google Fonts | Inter & Outfit typography, medical iconography |
| **BI Tooling** | Power BI Desktop | DAX measure library, Star Schema data modeling (optional) |
