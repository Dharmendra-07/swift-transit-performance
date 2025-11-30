"""
Data processing and flattening functionality for FedEx data
"""
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from config.constants import EVENT_CATEGORIES, WEIGHT_CONVERSIONS, DEFAULT_VALUES


class DataProcessor:
    """
    Processes nested FedEx JSON data into flat structure
    """
    
    def __init__(self):
        self.flattened_data = []
    
    def process_shipments(self, shipments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process all shipments
        """
        print(f"\n🔄 Processing {len(shipments)} shipments...")
        
        processed_count = 0
        for shipment in shipments:
            try:
                flattened = self._process_shipment(shipment)
                if flattened:
                    self.flattened_data.append(flattened)
                    processed_count += 1
            except Exception as e:
                print(f"⚠️  Failed to process shipment: {e}")
                continue
        
        print(f"✅ Processed {processed_count} shipments successfully")
        return self.flattened_data
    
    def _process_shipment(self, shipment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single FedEx shipment
        """
        # Basic info
        tracking_number = shipment.get('trackingNumber', 'UNKNOWN')
        carrier_code = shipment.get('carrierCode', 'UNKNOWN')
        
        # Service info
        service_info = shipment.get('service', {})
        service_type = service_info.get('type', 'UNKNOWN') if service_info else 'UNKNOWN'
        service_description = service_info.get('description', '') if service_info else ''
        
        # Package info
        package_info = shipment.get('package', {})
        weight_kg = self._extract_weight(package_info.get('weight', {}))
        packaging_type = package_info.get('packagingType', 'UNKNOWN')
        
        # Location info - handle FedEx address format
        origin_info = shipment.get('origin', {})
        dest_info = shipment.get('destination', {})
        
        origin_addr = self._extract_fedex_address(origin_info.get('address', {}))
        dest_addr = self._extract_fedex_address(dest_info.get('address', {}))
        
        # Process events
        events = shipment.get('events', [])
        processed_events = self._process_events(events)
        
        return {
            'tracking_number': tracking_number,
            'service_type': service_type,
            'service_description': service_description,
            'carrier_code': carrier_code,
            'package_weight_kg': weight_kg,
            'packaging_type': packaging_type,
            'origin_city': origin_addr['city'],
            'origin_state': origin_addr['state'],
            'origin_pincode': origin_addr['postal_code'],
            'destination_city': dest_addr['city'],
            'destination_state': dest_addr['state'],
            'destination_pincode': dest_addr['postal_code'],
            'events': processed_events,
            'delivery_location_type': shipment.get('deliveryLocationType', 'UNKNOWN')
        }
    
    def _process_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process events for a shipment
        """
        processed_events = []
        
        for event in events:
            try:
                timestamp = self._parse_timestamp(event.get('timestamp'))
                address = self._extract_fedex_address(event.get('address', {}))
                
                processed_event = {
                    'event_type': event.get('eventType', ''),
                    'timestamp': timestamp,
                    'description': event.get('eventDescription', ''),
                    'city': address['city'],
                    'state': address['state'],
                    'postal_code': address['postal_code'],
                    'arrival_location': event.get('arrivalLocation', ''),
                    'category': self._categorize_event(
                        event.get('eventType', ''), 
                        event.get('eventDescription', '')
                    )
                }
                processed_events.append(processed_event)
            except Exception:
                continue
        
        # Sort by timestamp (most recent first for FedEx data)
        processed_events.sort(key=lambda x: x['timestamp'] or datetime.min, reverse=False)
        return processed_events
    
    def _parse_timestamp(self, timestamp: Any) -> Optional[datetime]:
        """
        Parse timestamp from FedEx format ($numberLong)
        """
        if not timestamp:
            return None
        
        try:
            # Handle MongoDB $numberLong format (FedEx uses this)
            if isinstance(timestamp, dict) and '$numberLong' in timestamp:
                ts_ms = int(timestamp['$numberLong'])
                return datetime.fromtimestamp(ts_ms / 1000.0)
            
            # Handle string format as fallback
            elif isinstance(timestamp, str):
                # Clean the string
                ts_clean = re.sub(r'[+-]\d{2}:\d{2}$', '', timestamp)
                ts_clean = ts_clean.replace('Z', '').replace('T', ' ')
                
                # Try formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']:
                    try:
                        return datetime.strptime(ts_clean, fmt)
                    except ValueError:
                        continue
                
                return datetime.fromisoformat(ts_clean)
            
            # Numeric format
            elif isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp / 1000.0)
                
        except Exception:
            return None
        
        return None
    
    def _extract_weight(self, weight_info: Any) -> float:
        """
        Extract weight in kg from FedEx format
        """
        if not weight_info:
            return DEFAULT_VALUES['weight_kg']
        
        try:
            if isinstance(weight_info, dict):
                weight = weight_info.get('value', 0)
                unit = weight_info.get('units', '').lower()
                return weight * WEIGHT_CONVERSIONS.get(unit, 1.0)
            elif isinstance(weight_info, (int, float)):
                return float(weight_info)
        except Exception:
            pass
        
        return DEFAULT_VALUES['weight_kg']
    
    def _extract_fedex_address(self, address: Any) -> Dict[str, str]:
        """
        Extract address components from FedEx format
        """
        if not address or not isinstance(address, dict):
            return {'city': 'UNKNOWN', 'state': 'UNKNOWN', 'postal_code': 'UNKNOWN'}
        
        return {
            'city': address.get('city', 'UNKNOWN'),
            'state': address.get('stateOrProvinceCode', 'UNKNOWN'),
            'postal_code': address.get('postalCode', 'UNKNOWN')
        }
    
    def _categorize_event(self, event_type: str, description: str) -> str:
        """
        Categorize FedEx event types
        """
        text = (str(event_type) + ' ' + str(description)).upper()
        
        # FedEx specific event mappings
        fedex_categories = {
            'pickup': ['PU', 'PICKUP', 'PICKED UP'],
            'delivery': ['DL', 'DELIVERED'],
            'out_for_delivery': ['OD', 'ON FEDEX VEHICLE FOR DELIVERY'],
            'in_transit': ['IT', 'IN TRANSIT'],
            'arrival': ['AR', 'AT LOCAL FEDEX FACILITY', 'ARRIVED AT'],
            'departure': ['DP', 'LEFT FEDEX', 'DEPARTED'],
            'other': ['OC', 'SHIPMENT INFORMATION SENT']  # OC = Order Created
        }
        
        for category, keywords in fedex_categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'other'
    
    def get_flattened_data(self) -> List[Dict[str, Any]]:
        """Get processed data"""
        return self.flattened_data