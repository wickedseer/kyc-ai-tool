import re

def get_gst_data(list_name):
    registration_number_pattern = r'[A-Z0-9]{15}'
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    address_pattern = r'\b\d+\s*[-,\.]?\s*[A-Za-z0-9\s,-]+\b'

    data = {
        "registration_number": None,
        "legal_name": None,
        "trade_name": None,
        "date_of_liability": None,
        "date_of_issue": None,
        "address": None,
        "To": "NA",
        "CoB":"Proprietorship",
        "type_of_registration": None
    }

    for i, item in enumerate(list_name):
        if not data["registration_number"]:
            match = re.search(registration_number_pattern, item)
            if match:
                data["registration_number"] = match.group()

        if not data["legal_name"]:
            match = re.search(r'^\d*\.?\s*(Legal|Legat)\s*Name\s*$', item, re.IGNORECASE)
            if match:
                data["legal_name"] = list_name[i - 1]

        if not data["trade_name"]:
            match = re.search(r'^\d*\.?\s*(Trade\s*Name,\s*if\s*any)\s*$', item, re.IGNORECASE)
            if match:
                # Check previous and next items for trade name
                prev_item = list_name[i - 1] if i > 0 else None
                next_item = list_name[i + 1] if i < len(list_name) - 1 else None
                if prev_item and prev_item != data["legal_name"] and "Proprietorship" not in prev_item:
                    data["trade_name"] = prev_item
                elif next_item and next_item != data["legal_name"] and "Proprietorship" not in next_item:
                    data["trade_name"] = next_item

        if not data["date_of_liability"]:
            match = re.search(date_pattern, item)
            if match:
                data["date_of_liability"] = match.group()

        if not data["date_of_issue"]:
            match = re.search(date_pattern, item)
            if match:
                data["date_of_issue"] = match.group()

        if not data["address"]:
            match = re.search(r'^\d*\.?\s*(Address\s*of\s*Principal\s*Place\s*of)\s*$', item, re.IGNORECASE)
            if match:
                # Check both previous and next items for address
                prev_item = list_name[i - 1] if i > 0 else None
                next_item = list_name[i + 1] if i < len(list_name) - 1 else None
                if next_item:
                    data["address"] = next_item
                elif prev_item:
                    data["address"] = prev_item
                    
        if not data["type_of_registration"]:
            match = re.search(r'Type of Registration', item)
            if match:
                data["type_of_registration"] = list_name[i + 1] if i < len(list_name) - 1 else None

    return data