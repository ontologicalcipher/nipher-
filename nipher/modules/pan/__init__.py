import re

PAN_RE = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")

def run(target):
    pan = target.strip().upper().replace(" ", "")

    if not PAN_RE.fullmatch(pan):
        return {
            "module": "pan",
            "input": pan,
            "valid_format": False,
            "error": "Invalid PAN format. Expected ABCDE1234F."
        }

    category_map = {
        "P": "Individual",
        "C": "Company",
        "H": "HUF",
        "F": "Firm / LLP",
        "A": "Association of Persons",
        "T": "Trust",
        "B": "Body of Individuals",
        "L": "Local Authority",
        "J": "Artificial Juridical Person",
        "G": "Government"
    }

    return {
        "module": "pan",
        "input": pan[:3] + "*****" + pan[-2:],
        "valid_format": True,
        "category": category_map.get(pan[3], "Unknown"),
        "status": "Format validation successful",
        "note": "No private identity information is retrieved."
    }
