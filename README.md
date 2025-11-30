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

| tracking_number | service_type | carrier_code | package_weight_kg | packaging_type |
|----------------|--------------|--------------|--------------------|----------------|
| origin_city | origin_state | origin_pincode | destination_city | destination_state |
| origin_pincode | pickup_datetime_ist | delivery_datetime_ist | total_transit_hours | num_facilities_visited |
| num_in_transit_events | time_in_inter_facility_transit_hours | avg_hours_per_facility | is_express_service | delivery_location_type |
| num_out_for_delivery_attempts | first_attempt_delivery | total_events_count |

### 2️⃣ Summary  
`output/transit_performance_summary.csv`

| total_shipments | delivered | avg_delivery_hours | on_time_percent |
|----------------|-----------|---------------------|------------------|

---
 💾 EXPORT  
----------------------------------------
📄 Detailed -> output/transit_performance_detailed.csv  
📄 Summary  -> output/transit_performance_summary.csv  

🎉 DONE!
```

**🛠 Technologies Used**

- Python 3.10+
- Pandas  
- Datetime  
- Structured logging  


