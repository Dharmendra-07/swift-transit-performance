"""
Data loading and validation functionality for FedEx tracking data
"""
import json
import os
from typing import List, Dict, Any


class DataLoader:
    """
    Handles loading of FedEx tracking data from JSON files
    """
    
    def __init__(self):
        self.data = None
        self.validation_report = {}
    
    def load_data(self, file_path: str) -> bool:
        """
        Load JSON data from file and extract trackDetails
        """
        try:
            print(f"📥 Loading data from: {file_path}")
            
            if not os.path.exists(file_path):
                print(f"❌ Error: File '{file_path}' not found")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_data = json.load(file)
            
            # Extract trackDetails from each entry
            self.data = self._extract_shipments(raw_data)
            
            if not self._validate_data():
                return False
            
            print(f"✅ Successfully loaded {len(self.data)} shipments")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def _extract_shipments(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract shipment data from FedEx tracking response format
        """
        shipments = []
        
        for entry in raw_data:
            if 'trackDetails' in entry and entry['trackDetails']:
                for track_detail in entry['trackDetails']:
                    # Transform to our expected format
                    shipment = {
                        'trackingNumber': track_detail.get('trackingNumber'),
                        'carrierCode': track_detail.get('carrierCode'),
                        'service': track_detail.get('service', {}),
                        'package': {
                            'weight': track_detail.get('packageWeight', {}),
                            'packagingType': track_detail.get('packaging', {}).get('type', 'UNKNOWN')
                        },
                        'origin': {
                            'address': track_detail.get('shipperAddress', {})
                        },
                        'destination': {
                            'address': track_detail.get('destinationAddress', {})
                        },
                        'events': track_detail.get('events', []),
                        'deliveryLocationType': track_detail.get('deliveryLocationType', 'UNKNOWN')
                    }
                    shipments.append(shipment)
        
        return shipments
    
    def _validate_data(self) -> bool:
        """
        Validate the loaded data structure
        """
        if not self.data or not isinstance(self.data, list):
            print("❌ Invalid data format: Expected list of shipments")
            return False
        
        # Basic validation
        valid_shipments = 0
        total_events = 0
        unique_event_types = set()
        
        for shipment in self.data:
            if isinstance(shipment, dict) and shipment.get('events'):
                valid_shipments += 1
                total_events += len(shipment['events'])
                
                # Collect event types
                for event in shipment['events']:
                    if event.get('eventType'):
                        unique_event_types.add(event['eventType'])
        
        self.validation_report = {
            'total_shipments': len(self.data),
            'valid_shipments': valid_shipments,
            'total_events': total_events,
            'unique_event_types': list(unique_event_types)
        }
        
        print(f"📊 Validation Report:")
        print(f"   • Total shipments: {len(self.data)}")
        print(f"   • Valid shipments: {valid_shipments}")
        print(f"   • Total events: {total_events}")
        print(f"   • Event types: {list(unique_event_types)}")
        
        return valid_shipments > 0
    
    def get_data(self) -> List[Dict[str, Any]]:
        """Get loaded data"""
        return self.data or []
    
    def explore_sample(self) -> None:
        """Explore sample data structure"""
        if not self.data:
            return
        
        print(f"\n🔍 Sample Data Structure:")
        print("-" * 40)
        
        sample = self.data[0]
        print(f"Tracking: {sample.get('trackingNumber', 'N/A')}")
        print(f"Service: {sample.get('service', {}).get('type', 'N/A')}")
        print(f"Carrier: {sample.get('carrierCode', 'N/A')}")
        print(f"Events: {len(sample.get('events', []))}")
        
        if sample.get('events'):
            print(f"First event: {sample['events'][0].get('eventType', 'N/A')}")
            print(f"First event timestamp: {sample['events'][0].get('timestamp', 'N/A')}")