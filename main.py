#!/usr/bin/env python3
"""
SWIFT Transit Performance Analysis
Main application
"""

import os
import sys
import time

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.metrics_calculator import MetricsCalculator
from src.output_generator import OutputGenerator


def main():
    """
    Main function
    """
    start_time = time.time()
    
    print("🚀 SWIFT Transit Performance Analysis")
    print("=" * 60)
    print()
    
    # Step 1: Initialize components
    data_loader = DataLoader()
    data_processor = DataProcessor()
    metrics_calculator = MetricsCalculator()
    output_generator = OutputGenerator()
    
    # Step 2: Load data
    data_file = 'data/shipment_data.json'
    
    print("1. 📥 LOADING DATA")
    print("-" * 40)
    
    if not data_loader.load_data(data_file):
        print("❌ Cannot proceed without data")
        return 1
    
    data_loader.explore_sample()
    raw_data = data_loader.get_data()
    
    # Step 3: Process data
    print("\n2. 🔄 PROCESSING DATA")
    print("-" * 40)
    
    flattened_data = data_processor.process_shipments(raw_data)
    
    if not flattened_data:
        print("❌ No data processed")
        return 1
    
    # Step 4: Calculate metrics
    print("\n3. 📊 CALCULATING METRICS")
    print("-" * 40)
    
    performance_metrics = metrics_calculator.calculate_metrics(flattened_data)
    
    if not performance_metrics:
        print("❌ No metrics calculated")
        return 1
    
    # Step 5: Generate outputs
    print("\n4. 📁 GENERATING OUTPUTS")
    print("-" * 40)
    
    # Create CSV files
    detailed_file = output_generator.generate_detailed_csv(performance_metrics)
    summary_file = output_generator.generate_summary_csv(performance_metrics)
    
    # Print report
    output_generator.print_report(performance_metrics)
    
    # Final summary
    execution_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 60)
    
    print(f"\n📊 RESULTS:")
    print(f"   • Processed shipments: {len(performance_metrics)}")
    print(f"   • Execution time: {execution_time:.2f} seconds")
    
    print(f"\n📁 OUTPUT FILES:")
    if detailed_file and os.path.exists(detailed_file):
        size = os.path.getsize(detailed_file) / 1024
        print(f"   • Detailed CSV: {detailed_file} ({size:.1f} KB)")
    
    if summary_file and os.path.exists(summary_file):
        size = os.path.getsize(summary_file) / 1024
        print(f"   • Summary CSV: {summary_file} ({size:.1f} KB)")
    
    print(f"\n🛡️  EDGE CASES HANDLED:")
    cases = [
        "Missing/null values",
        "Various timestamp formats", 
        "Incomplete event sequences",
        "Missing address information",
        "Duplicate events",
        "Empty events arrays",
        "Nested field variations"
    ]
    
    for case in cases:
        print(f"   ✓ {case}")
    
    print(f"\n🎉 Success! Check the 'output' folder for your CSV files.")
    
    return 0


if __name__ == "__main__":
    # Check if data file exists
    if not os.path.exists('data/shipment_data.json'):
        print("❌ Error: data/shipment_data.json not found")
        print("Please ensure your JSON file is in the data/ directory")
        sys.exit(1)
    
    # Run the analysis
    exit_code = main()
    sys.exit(exit_code)