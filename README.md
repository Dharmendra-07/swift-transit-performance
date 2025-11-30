**SWIFT Transit Performance Analysis**

A comprehensive solution for analyzing FedEx courier logistics transit performance using tracking data from the FedEx API.

**📋 Project Overview**

This project processes FedEx shipment tracking data to calculate transit performance metrics, facility touchpoints, delivery efficiency, and generate comprehensive analytics reports. The solution handles real-world FedEx API response format with robust error handling for production use.



**🏗️ Project Structure**

swift-transit-analysis/
│
├── src/                    # Source code modules
│   ├── __init__.py
│   ├── data_loader.py      # FedEx data loading and extraction
│   ├── data_processor.py   # Data processing and flattening
│   ├── metrics_calculator.py # Performance metrics calculation
│   └── output_generator.py # CSV and report generation
│
├── config/                 # Configuration files
│   ├── __init__.py
│   └── constants.py        # FedEx-specific constants and mappings
│
├── data/                   # Input data directory
│   └── shipment_data.json  # Your FedEx tracking data
│
├── output/                 # Generated analysis files
│   ├── transit_performance_detailed.csv
│   └── transit_performance_summary.csv
│
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file

**🚀 Quick Start**

**Prerequisites**

Python 3.7+

pip (Python package manager)

**Installation**

1. Clone or download the project:

# If using git
git clone <repository-url>
cd swift-transit-analysis

# Or create the directory structure manually
mkdir swift-transit-analysis
cd swift-transit-analysis

2. Install dependencies:

pip install -r requirements.txt

requirements.txt

pandas>=1.5.0
numpy>=1.21.0
python-dateutil>=2.8.0

**3. Prepare your data:**

Place your FedEx shipment_data.json file in the data/ directory

Ensure the JSON file contains FedEx tracking API responses


**Usage**

**Run the full analysis:**

python main.py



**📊 Output Files**

After running the analysis, you'll get:

**1. output/transit_performance_detailed.csv**

Shipment-level data for each tracking number

Transit times, facility visits, delivery performance

23 columns of detailed metrics

**2. output/transit_performance_summary.csv**

Network-wide performance statistics

Service type comparisons

Delivery success rates

Facility efficiency metrics