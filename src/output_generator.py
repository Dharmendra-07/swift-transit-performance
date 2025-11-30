"""
Output generation for CSV files
"""
import pandas as pd
import numpy as np
import os
from typing import List, Dict, Any


class OutputGenerator:
    """
    Generates output CSV files
    """
    
    def __init__(self):
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create output directories"""
        os.makedirs('output', exist_ok=True)
        print("✅ Created output directory")
    
    def generate_detailed_csv(self, metrics: List[Dict[str, Any]]) -> str:
        """
        Generate detailed CSV file
        """
        if not metrics:
            print("❌ No metrics for detailed CSV")
            return ""
        
        output_file = 'output/transit_performance_detailed.csv'
        
        print(f"\n💾 Creating detailed CSV: {output_file}")
        
        df = pd.DataFrame(metrics)
        
        # Format datetime columns
        for col in ['pickup_datetime_ist', 'delivery_datetime_ist']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Ensure numeric columns
        numeric_cols = [
            'package_weight_kg', 'total_transit_hours', 'num_facilities_visited',
            'num_in_transit_events', 'time_in_inter_facility_transit_hours',
            'avg_hours_per_facility', 'num_out_for_delivery_attempts', 'total_events_count'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Required columns in order
        required_columns = [
            'tracking_number', 'service_type', 'carrier_code', 'package_weight_kg',
            'packaging_type', 'origin_city', 'origin_state', 'origin_pincode',
            'destination_city', 'destination_state', 'destination_pincode',
            'pickup_datetime_ist', 'delivery_datetime_ist', 'total_transit_hours',
            'num_facilities_visited', 'num_in_transit_events',
            'time_in_inter_facility_transit_hours', 'avg_hours_per_facility',
            'is_express_service', 'delivery_location_type',
            'num_out_for_delivery_attempts', 'first_attempt_delivery', 'total_events_count'
        ]
        
        # Keep only existing columns
        final_columns = [col for col in required_columns if col in df.columns]
        df = df[final_columns]
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print(f"✅ Detailed CSV created: {output_file}")
        print(f"   📊 Records: {len(df)}")
        print(f"   📋 Columns: {len(df.columns)}")
        
        return output_file
    
    def generate_summary_csv(self, metrics: List[Dict[str, Any]]) -> str:
        """
        Generate summary CSV file
        """
        if not metrics:
            print("❌ No metrics for summary CSV")
            return ""
        
        output_file = 'output/transit_performance_summary.csv'
        
        print(f"\n💾 Creating summary CSV: {output_file}")
        
        df = pd.DataFrame(metrics)
        summary_data = []
        
        def safe_stats(series):
            """Safe statistics calculation"""
            clean = pd.to_numeric(series, errors='coerce').dropna()
            if len(clean) == 0:
                return 0.0, 0.0, 0.0, 0.0, 0.0
            return (
                float(clean.mean()),
                float(clean.median()),
                float(clean.std()),
                float(clean.min()),
                float(clean.max())
            )
        
        # Overall Metrics
        total_shipments = len(df)
        avg_transit, median_transit, std_transit, min_transit, max_transit = safe_stats(df['total_transit_hours'])
        
        summary_data.extend([
            {'metric_category': 'Overall Metrics', 'metric_name': 'total_shipments_analyzed', 'metric_value': total_shipments},
            {'metric_category': 'Overall Metrics', 'metric_name': 'avg_transit_hours', 'metric_value': round(avg_transit, 4)},
            {'metric_category': 'Overall Metrics', 'metric_name': 'median_transit_hours', 'metric_value': round(median_transit, 4)},
            {'metric_category': 'Overall Metrics', 'metric_name': 'std_dev_transit_hours', 'metric_value': round(std_transit, 4)},
            {'metric_category': 'Overall Metrics', 'metric_name': 'min_transit_hours', 'metric_value': round(min_transit, 4)},
            {'metric_category': 'Overall Metrics', 'metric_name': 'max_transit_hours', 'metric_value': round(max_transit, 4)}
        ])
        
        # Facility Metrics
        avg_facilities, median_facilities, _, _, _ = safe_stats(df['num_facilities_visited'])
        avg_hours_facility, median_hours_facility, _, _, _ = safe_stats(df['avg_hours_per_facility'])
        
        # Mode calculation
        mode_value = float(df['num_facilities_visited'].mode().iloc[0]) if not df['num_facilities_visited'].mode().empty else 0.0
        
        summary_data.extend([
            {'metric_category': 'Facility Metrics', 'metric_name': 'avg_facilities_per_shipment', 'metric_value': round(avg_facilities, 4)},
            {'metric_category': 'Facility Metrics', 'metric_name': 'median_facilities_per_shipment', 'metric_value': round(median_facilities, 4)},
            {'metric_category': 'Facility Metrics', 'metric_name': 'mode_facilities_per_shipment', 'metric_value': mode_value},
            {'metric_category': 'Facility Metrics', 'metric_name': 'avg_hours_per_facility', 'metric_value': round(avg_hours_facility, 4)},
            {'metric_category': 'Facility Metrics', 'metric_name': 'median_hours_per_facility', 'metric_value': round(median_hours_facility, 4)}
        ])
        
        # Service Type Comparison
        for service_type, group in df.groupby('service_type'):
            service_avg_transit, _, _, _, _ = safe_stats(group['total_transit_hours'])
            service_avg_facilities, _, _, _, _ = safe_stats(group['num_facilities_visited'])
            
            summary_data.extend([
                {'metric_category': f'Service Type: {service_type}', 'metric_name': 'avg_transit_hours_by_service_type', 'metric_value': round(service_avg_transit, 4)},
                {'metric_category': f'Service Type: {service_type}', 'metric_name': 'avg_facilities_by_service_type', 'metric_value': round(service_avg_facilities, 4)},
                {'metric_category': f'Service Type: {service_type}', 'metric_name': 'count_shipments_by_service_type', 'metric_value': len(group)}
            ])
        
        # Delivery Performance
        first_attempt_rate = df['first_attempt_delivery'].mean() * 100
        avg_attempts = df['num_out_for_delivery_attempts'].mean()
        
        summary_data.extend([
            {'metric_category': 'Delivery Performance', 'metric_name': 'pct_first_attempt_delivery', 'metric_value': round(first_attempt_rate, 4)},
            {'metric_category': 'Delivery Performance', 'metric_name': 'avg_out_for_delivery_attempts', 'metric_value': round(avg_attempts, 4)}
        ])
        
        # Create and save summary
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(output_file, index=False)
        
        print(f"✅ Summary CSV created: {output_file}")
        print(f"   📊 Metrics: {len(summary_df)}")
        
        return output_file
    
    def print_report(self, metrics: List[Dict[str, Any]]) -> None:
        """
        Print analysis report
        """
        if not metrics:
            return
        
        df = pd.DataFrame(metrics)
        
        print("\n" + "="*50)
        print("📋 ANALYSIS REPORT")
        print("="*50)
        
        print(f"📦 Total Shipments: {len(df):,}")
        
        # Service distribution
        service_dist = df['service_type'].value_counts()
        print(f"\n🎯 Service Distribution:")
        for service, count in service_dist.items():
            pct = (count / len(df)) * 100
            print(f"   {service}: {count} ({pct:.1f}%)")
        
        # Performance summary
        print(f"\n⏱️  Transit Performance:")
        print(f"   Average: {df['total_transit_hours'].mean():.2f} hours")
        print(f"   Median: {df['total_transit_hours'].median():.2f} hours")
        
        print(f"\n🏢 Facility Performance:")
        print(f"   Avg Facilities: {df['num_facilities_visited'].mean():.2f}")
        
        print(f"\n📮 Delivery Performance:")
        first_attempt = df['first_attempt_delivery'].mean() * 100
        print(f"   First Attempt: {first_attempt:.1f}%")