"""
Configuration constants for FedEx transit performance analysis
"""

# FedEx specific event type mappings
EVENT_CATEGORIES = {
    'pickup': ['PU', 'PICKUP', 'PICKED UP'],
    'delivery': ['DL', 'DELIVERED'],
    'out_for_delivery': ['OD', 'ON FEDEX VEHICLE FOR DELIVERY', 'OUT FOR DELIVERY'],
    'in_transit': ['IT', 'IN TRANSIT'],
    'arrival': ['AR', 'AT LOCAL FEDEX FACILITY', 'ARRIVED AT', 'AT DESTINATION'],
    'departure': ['DP', 'LEFT FEDEX', 'DEPARTED'],
    'other': ['OC', 'SHIPMENT INFORMATION SENT']
}

# Express service identifiers for FedEx
EXPRESS_SERVICES = [
    'FEDEX_EXPRESS_SAVER',
    'FEDEX_2_DAY',
    'FEDEX_2_DAY_AM',
    'FEDEX_STANDARD_OVERNIGHT',
    'FEDEX_PRIORITY_OVERNIGHT',
    'FEDEX_FIRST_OVERNIGHT',
    'EXPRESS'
]

# FedEx facility keywords
FACILITY_KEYWORDS = [
    'FACILITY', 
    'FEDEX_FACILITY', 
    'DESTINATION_FEDEX_FACILITY',
    'ORIGIN_FEDEX_FACILITY',
    'STATION',
    'HUB'
]

# Weight conversion factors
WEIGHT_CONVERSIONS = {
    'g': 0.001,
    'lb': 0.453592,
    'lbs': 0.453592,
    'kg': 1.0
}

# Default values
DEFAULT_VALUES = {
    'weight_kg': 0.0,
    'transit_hours': 0.0,
    'facilities': 0,
    'events': 0
}

# FedEx specific carrier codes
CARRIER_MAPPINGS = {
    'FDXE': 'FedEx Express',
    'FDXG': 'FedEx Ground'
}