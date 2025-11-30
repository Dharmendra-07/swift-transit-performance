# 🚀 SWIFT Transit Performance Analyzer

A complete end-to-end Python project for analyzing shipment performance, delivery delays, and transit efficiency.

---

## 📌 Overview

**SWIFT Transit Performance Analyzer** processes shipment events and automatically generates:

- Cleaned & validated shipment data  
- Per-shipment performance metrics  
- Summary KPIs (avg delivery time, delays, on-time %)  
- CSV exports for dashboards or analysis  

Run a single command:

```bash
python3 main.py
```

---

## 📂 Project Structure

```
swift-transit-performance/
│
├── data/
│   └── shipment_data.json
│
├── output/
│   ├── transit_performance_detailed.csv
│   └── transit_performance_summary.csv
│
├── services/
│   ├── data_loader.py
│   ├── event_processing.py
│   ├── performance_calculator.py
│   └── utils.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

Place your file:

```
data/shipment_data.json
```

Then run:

```bash
python3 main.py
```

Example output:

```
🚀 SWIFT Transit Performance Analysis
📥 Loading data from: data/shipment_data.json  
📊 Validation Report:
   • Total shipments: 95
   • Valid shipments: 95
   • Total events: 1,243
```

---

## 📤 Output Files

### 1️⃣ Detailed Performance  
`output/transit_performance_detailed.csv`

Columns include:

| shipment_id | first_scan | delivered_at | total_hours | status | delayed_by_hrs |
|-------------|------------|---------------|-------------|--------|----------------|

---

### 2️⃣ Summary  
`output/transit_performance_summary.csv`

| total_shipments | delivered | avg_delivery_hours | on_time_percent |
|----------------|-----------|---------------------|------------------|

---

## 🧪 Example Command Result

```
🚀 SWIFT Transit Performance Analysis
============================================================

1. 📥 LOADING DATA  
----------------------------------------
📥 Loading data from: data/shipment_data.json  
📊 Validation Report:
   • Total shipments: 95
   • Valid shipments: 95
   • Total events: 1,243
   • Event types: ['ARRIVED', 'DISPATCHED', 'OFD', 'DELIVERED']

2. ⚙️ PROCESSING SHIPMENT EVENTS  
----------------------------------------

3. 📈 CALCULATING SUMMARY KPIs  
----------------------------------------

4. 💾 EXPORT  
----------------------------------------
📄 Detailed -> output/transit_performance_detailed.csv  
📄 Summary  -> output/transit_performance_summary.csv  

🎉 DONE!
```

---

## 🧹 Fix for "Valid shipments: 0" Issue

If you see:

```
Valid shipments: 0
Cannot proceed without data
```

Your JSON format is wrong.

Use this format:

```json
[
  {
    "shipment_id": "SWF123",
    "events": [
      { "event_type": "ARRIVED", "timestamp": "2025-01-21T10:00:00" },
      { "event_type": "DEPARTED", "timestamp": "2025-01-21T14:30:00" },
      { "event_type": "DELIVERED", "timestamp": "2025-01-22T09:50:00" }
    ]
  }
]
```

---

## 🛠 Technologies Used

- Python 3.10+
- Pandas  
- Datetime  
- Structured logging  

---

## 💬 Need More Features?

If you want:

- JSON generator  
- Fake data creator  
- API ingestion  
- Database integration  
- Visualization dashboards  

Tell me — I’ll build the next module.

---
