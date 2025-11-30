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

This file contains one row per shipment with complete transit analytics.

#### 📌 Columns Included

| Column Name | Description |
|------------|-------------|
| **tracking_number** | Unique FedEx tracking number |
| **service_type** | Shipping service (e.g., Express, Economy) |
| **carrier_code** | FedEx carrier code (FDXE, FDXG, etc.) |
| **package_weight_kg** | Weight of the package in kilograms |
| **packaging_type** | Type of packaging used |
| **origin_city** | Origin city name |
| **origin_state** | Origin state/province |
| **origin_pincode** | Origin postal code |
| **destination_city** | Destination city name |
| **destination_state** | Destination state/province |
| **destination_pincode** | Destination postal code |
| **pickup_datetime_ist** | Pickup timestamp (converted to IST) |
| **delivery_datetime_ist** | Delivery timestamp (converted to IST) |
| **total_transit_hours** | Total delivery time in hours |
| **num_facilities_visited** | Number of FedEx facilities scanned through |
| **num_in_transit_events** | Count of "In Transit" events |
| **time_in_inter_facility_transit_hours** | Hours spent between facilities |
| **avg_hours_per_facility** | Avg processing time per facility |
| **is_express_service** | Whether shipment used an express service (Yes/No) |
| **delivery_location_type** | Residential/Commercial classification |
| **num_out_for_delivery_attempts** | Number of OFD events |
| **first_attempt_delivery** | Delivered on first attempt? (True/False) |
| **total_events_count** | Total number of tracking events |

---
### 2️⃣ Summary Performance  
`output/transit_performance_summary.csv`

This file provides **aggregated network-level performance metrics** across all shipments.

#### 📊 Columns Included

**Overall Metrics**

| Column Name | Description |
|------------|-------------|
| **total_shipments_analyzed** | Total number of shipments processed |
| **avg_transit_hours** | Average total transit time (in hours) |
| **median_transit_hours** | Median total transit time (in hours) |
| **std_dev_transit_hours** | Standard deviation of transit times |
| **min_transit_hours** | Shortest transit time recorded |
| **max_transit_hours** | Longest transit time recorded |

**Facility Metrics**

| Column Name | Description |
|------------|-------------|
| **avg_facilities_per_shipment** | Average number of facilities visited per shipment |
| **median_facilities_per_shipment** | Median number of facilities visited |
| **mode_facilities_per_shipment** | Most common number of facilities visited |
| **avg_hours_per_facility** | Average hours spent at each facility |
| **median_hours_per_facility** | Median hours spent per facility |

**Service Type Comparison** *(Grouped by `service.type`)*

| Column Name | Description |
|------------|-------------|
| **avg_transit_hours_by_service_type** | Average transit hours for each service type |
| **avg_facilities_by_service_type** | Average facilities visited for each service type |
| **count_shipments_by_service_type** | Number of shipments for each service type |

**Delivery Performance**

| Column Name | Description |
|------------|-------------|
| **pct_first_attempt_delivery** | Percentage of shipments delivered on the first attempt |
| **avg_out_for_delivery_attempts** | Average number of “out for delivery” attempts per shipment |

---

This summary CSV complements the **detailed shipment-level CSV** to provide both **per-shipment insights** and **network-wide KPIs**, making it ideal for dashboards, reports, or analytics.

---
 💾 EXPORT  
----------------------------------------
📄 Detailed -> output/transit_performance_detailed.csv  
📄 Summary  -> output/transit_performance_summary.csv  

🎉 DONE!


**🛠 Technologies Used**
```
- Python 3.10+
- Pandas  
- Datetime  
- Structured logging
