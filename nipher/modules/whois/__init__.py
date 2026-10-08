import socket
from datetime import datetime, timezone


def run(target, **kwargs):
    target = target.strip().lower()

    if not target:
        raise ValueError("Domain cannot be empty")

    try:
        import whois
    except ImportError:
        return {
            "success": False,
            "module": "whois",
            "target": target,
            "error": "python-whois is not installed"
        }

    try:
        data = whois.whois(target)

        def clean(value):
            if isinstance(value, (list, tuple)):
                return [str(v) for v in value]
            if value is None:
                return None
            return str(value)

        return {
            "success": True,
            "module": "whois",
            "target": target,
            "domain_name": clean(data.domain_name),
            "registrar": clean(data.registrar),
            "creation_date": clean(data.creation_date),
            "expiration_date": clean(data.expiration_date),
            "updated_date": clean(data.updated_date),
            "name_servers": clean(data.name_servers),
            "status": clean(data.status),
            "emails": clean(data.emails),
        }

    except Exception as e:
        return {
            "success": False,
            "module": "whois",
            "target": target,
            "error": str(e)
        }
