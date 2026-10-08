import phonenumbers
from phonenumbers import geocoder, carrier, timezone

def run(target):
    try:
        n=phonenumbers.parse(target,"IN")
        return {
            "module":"number",
            "input":target,
            "international":phonenumbers.format_number(n,phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "national":phonenumbers.format_number(n,phonenumbers.PhoneNumberFormat.NATIONAL),
            "country_code":n.country_code,
            "national_number":n.national_number,
            "valid":phonenumbers.is_valid_number(n),
            "possible":phonenumbers.is_possible_number(n),
            "region":phonenumbers.region_code_for_number(n),
            "location":geocoder.description_for_number(n,"en"),
            "carrier":carrier.name_for_number(n,"en"),
            "timezones":list(timezone.time_zones_for_number(n))
        }
    except Exception as e:
        return {"module":"number","input":target,"error":str(e)}
