street_schema = {
    "type": "object",
    "properties": {
        "long": {"type": "number"},
        "lat": {"type": "number"},
    }
}
street_schema_result = {
    "type": "object",
    "properties": {
        "location": {"type": "object",
                     "properties": {
                         "lng": {"type": "number"},
                         "lat": {"type": "number"},
                     }},
        "accuracy": {"type": "number"},
    }
}

geo_schema = {
    "type": "object",
    "properties": {
        "homeMobileCountryCode": {"type": "number"},
        "homeMobileNetworkCode": {"type": "number"},
        "considerIp": {"type": "boolean"},
        "carrier": {"type": "string"},
        "cellTowers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "cellId": {"type": "number"},
                    "locationAreaCode": {"type": "number"},
                    "mobileCountryCode": {"type": "number"},
                    "mobileNetworkCode": {"type": "number"},
                }
            }
        }
    }
}
geo_schema_result = {
    "type": "object",
    "properties": {
        "snappedPoints": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "object",
                        "properties": {
                            "latitude": {"type": "number"},
                            "longitude": {"type": "number"},
                        }
                    },
                    "originalIndex": {"type": "number"},
                    "placeId": {"type": "string"},
                }
            }
        }
    }
}
