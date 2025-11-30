"""
Transit performance metrics calculation
"""
from typing import List, Dict, Any
from config.constants import FACILITY_KEYWORDS, EXPRESS_SERVICES


class MetricsCalculator:
    """
    Calculates transit performance metrics
    """
    
    def __init__(self):
        self.performance_metrics = []
    
    def calculate_metrics(self, flattened_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate metrics for all shipments
        """
        print(f"\n📈 Calculating metrics for {len(flattened_data)} shipments...")
        
        calculated_count = 0
        for shipment in flattened_data:
            try:
                metrics = self._calculate_shipment_metrics(shipment)
                if metrics:
                    self.performance_metrics.append(metrics)
                    calculated_count += 1
            except Exception as e:
                print(f"⚠️  Failed to calculate metrics: {e}")
                continue
        
        print(f"✅ Calculated metrics for {calculated_count} shipments")
        return self.performance_metrics
    
    def _calculate_shipment_metrics(self, shipment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate metrics for a single shipment
        """
        events = shipment['events']
        valid_events = [e for e in events if e.get('timestamp')]
        
        if len(valid_events) < 2:
            return None
        
        # Facility metrics
        facility_metrics = self._calculate_facility_metrics(valid_events)
        
        # Time metrics
        time_metrics = self._calculate_time_metrics(valid_events)
        
        # Service classification
        is_express = any(
            express_word in str(shipment['service_type']).upper() 
            for express_word in EXPRESS_SERVICES
        )
        
        # Delivery metrics
        delivery_metrics = self._calculate_delivery_metrics(valid_events)
        
        # Build metrics dictionary
        metrics = {
            # Basic info
            'tracking_number': shipment['tracking_number'],
            'service_type': shipment['service_type'],
            'carrier_code': shipment['carrier_code'],
            'package_weight_kg': round(shipment['package_weight_kg'], 2),
            'packaging_type': shipment['packaging_type'],
            
            # Location info
            'origin_city': shipment['origin_city'],
            'origin_state': shipment['origin_state'],
            'origin_pincode': shipment['origin_pincode'],
            'destination_city': shipment['destination_city'],
            'destination_state': shipment['destination_state'],
            'destination_pincode': shipment['destination_pincode'],
            
            # Time metrics
            'pickup_datetime_ist': time_metrics['pickup_time'],
            'delivery_datetime_ist': time_metrics['delivery_time'],
            'total_transit_hours': round(time_metrics['total_hours'], 2),
            'time_in_inter_facility_transit_hours': round(time_metrics['inter_facility_hours'], 2),
            
            # Facility metrics
            'num_facilities_visited': facility_metrics['unique_facilities'],
            'num_in_transit_events': facility_metrics['in_transit_events'],
            
            # Velocity metrics
            'avg_hours_per_facility': round(
                time_metrics['total_hours'] / facility_metrics['unique_facilities'] 
                if facility_metrics['unique_facilities'] > 0 else 0, 2
            ),
            
            # Service classification
            'is_express_service': is_express,
            
            # Delivery metrics
            'delivery_location_type': shipment['delivery_location_type'],
            'num_out_for_delivery_attempts': delivery_metrics['attempts'],
            'first_attempt_delivery': delivery_metrics['first_attempt'],
            
            # Event counts
            'total_events_count': len(valid_events)
        }
        
        return metrics
    
    def _calculate_facility_metrics(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate facility-related metrics
        """
        facility_events = [
            e for e in events 
            if any(keyword in str(e.get('arrival_location', '')).upper() 
                  for keyword in FACILITY_KEYWORDS)
        ]
        
        # Unique facilities
        unique_facilities = set()
        for event in facility_events:
            key = f"{event.get('city')}_{event.get('state')}_{event.get('postal_code')}"
            if key.strip('_'):
                unique_facilities.add(key)
        
        # In-transit events
        in_transit_events = len([e for e in events if e.get('category') == 'in_transit'])
        
        return {
            'unique_facilities': len(unique_facilities),
            'in_transit_events': in_transit_events
        }
    
    def _calculate_time_metrics(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate time-related metrics
        """
        pickup_events = [e for e in events if e.get('category') == 'pickup']
        delivery_events = [e for e in events if e.get('category') == 'delivery']
        
        pickup_time = pickup_events[0]['timestamp'] if pickup_events else None
        delivery_time = delivery_events[-1]['timestamp'] if delivery_events else None
        
        # Total transit time
        total_hours = 0.0
        if pickup_time and delivery_time:
            delta = delivery_time - pickup_time
            total_hours = max(0.0, delta.total_seconds() / 3600)
        
        # Inter-facility time
        inter_facility_hours = self._calculate_inter_facility_time(events)
        
        return {
            'pickup_time': pickup_time,
            'delivery_time': delivery_time,
            'total_hours': total_hours,
            'inter_facility_hours': inter_facility_hours
        }
    
    def _calculate_inter_facility_time(self, events: List[Dict[str, Any]]) -> float:
        """
        Calculate time between facilities
        """
        facility_events = [
            e for e in events 
            if any(keyword in str(e.get('arrival_location', '')).upper() 
                  for keyword in FACILITY_KEYWORDS)
        ]
        
        if len(facility_events) < 2:
            return 0.0
        
        sorted_events = sorted(facility_events, key=lambda x: x['timestamp'])
        first_time = sorted_events[0]['timestamp']
        last_time = sorted_events[-1]['timestamp']
        
        delta = last_time - first_time
        return max(0.0, delta.total_seconds() / 3600)
    
    def _calculate_delivery_metrics(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate delivery-related metrics
        """
        out_for_delivery = [e for e in events if e.get('category') == 'out_for_delivery']
        attempts = len(out_for_delivery)
        first_attempt = attempts <= 1
        
        return {
            'attempts': attempts,
            'first_attempt': first_attempt
        }
    
    def get_performance_metrics(self) -> List[Dict[str, Any]]:
        """Get calculated metrics"""
        return self.performance_metrics