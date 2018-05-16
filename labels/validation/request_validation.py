get_label_schema = {
    "type": "object",
    "required": ["serialNumber"],
    "properties": {
        "serialNumber": {"type": "string"},
        "exist": {"type": "boolean"},
        "imei1": {"type": ["string", "null"]},
        "imei2": {"type": ["string", "null"]},
        "pcbSerialNumber": {"type": "string"},
        "tagInfo": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "additionalInfo": {"type": ["string", "null"]},
                "ceLab": {"type": "string"},
                "chargerInfo": {"type": "string"},
                "countriesTable": {"type": ["string", "null"]},
                "customerIdType": {"type": ["string", "null"]},
                "customerIdValue": {"type": ["string", "null"]},
                "customerName": {"type": ["string", "null"]},
                "eanBq": {"type": "string"},
                "eanInLabel": {"type": ["boolean", "null"]},
                "eanOutlet": {"type": "string"},
                "freeMemory": {"type": ["string", "null"]},
                "imeisConfig": {"type": "string"},
                "labelType": {"type": "string"},
                "productColor": {"type": "string"},
                "productName": {"type": "string"},
                "showAssemblyDate": {"type": "boolean"},
                "skuOutlet": {"type": "string"},
                "tuvLogo": {"type": "boolean"},
                "warning": {"type": "boolean"}
            }
        }
    }
}
