import os
import requests
from urllib.parse import quote

TIMEOUT = 20

def _celestrak(target):
    target = target.strip()

    if target.isdigit():
        params = {"CATNR": target, "FORMAT": "JSON"}
    else:
        params = {"NAME": target, "FORMAT": "JSON"}

    r = requests.get(
        "https://celestrak.org/NORAD/elements/gp.php",
        params=params,
        headers={"User-Agent": "NIPHER/0.1"},
        timeout=TIMEOUT
    )

    if not r.ok:
        return {
            "source": "CelesTrak",
            "status": r.status_code,
            "error": r.text[:500]
        }

    data = r.json()

    if isinstance(data, dict):
        data = [data]

    satellites = []

    for x in data[:25]:
        satellites.append({
            "name": x.get("OBJECT_NAME"),
            "norad_id": x.get("NORAD_CAT_ID"),
            "international_designator": x.get("OBJECT_ID"),
            "epoch": x.get("EPOCH"),
            "mean_motion": x.get("MEAN_MOTION"),
            "eccentricity": x.get("ECCENTRICITY"),
            "inclination_deg": x.get("INCLINATION"),
            "raan_deg": x.get("RA_OF_ASC_NODE"),
            "arg_perigee_deg": x.get("ARG_OF_PERICENTER"),
            "mean_anomaly_deg": x.get("MEAN_ANOMALY"),
            "tle_available": True
        })

    return {
        "source": "CelesTrak",
        "query": target,
        "count": len(satellites),
        "satellites": satellites
    }


def _satnogs(target):
    url = "https://db.satnogs.org/api/satellites/"

    r = requests.get(
        url,
        params={"search": target},
        headers={"User-Agent": "NIPHER/0.1"},
        timeout=TIMEOUT
    )

    if not r.ok:
        return {
            "source": "SatNOGS",
            "status": r.status_code,
            "error": r.text[:500]
        }

    data = r.json()

    if isinstance(data, dict):
        results = data.get("results", [])
    else:
        results = data

    satellites = []

    for x in results[:25]:
        satellites.append({
            "name": x.get("name"),
            "norad_id": x.get("norad_cat_id"),
            "satellite_id": x.get("sat_id"),
            "status": x.get("status"),
            "operator": x.get("operator"),
            "alternative_names": x.get("names"),
            "website": x.get("website"),
            "transmitters": x.get("transmitters")
        })

    return {
        "source": "SatNOGS",
        "query": target,
        "count": len(satellites),
        "satellites": satellites
    }


def _n2yo(target):
    key = os.getenv("N2YO_API_KEY")

    if not key:
        return {
            "source": "N2YO",
            "status": "not_configured",
            "message": "Set N2YO_API_KEY to enable this provider."
        }

    if not target.isdigit():
        return {
            "source": "N2YO",
            "error": "N2YO requires a NORAD catalog ID."
        }

    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{target}"

    r = requests.get(
        url,
        params={"apiKey": key},
        headers={"User-Agent": "NIPHER/0.1"},
        timeout=TIMEOUT
    )

    if not r.ok:
        return {
            "source": "N2YO",
            "status": r.status_code,
            "error": r.text[:500]
        }

    data = r.json()

    return {
        "source": "N2YO",
        "satellite": data.get("info"),
        "tle": data.get("tle")
    }


def run(target):
    target = target.strip()

    if not target:
        return {"module": "satellite_intel", "error": "Target required"}

    results = {
        "module": "satellite_intel",
        "target": target,
        "providers": []
    }

    try:
        results["providers"].append(_celestrak(target))
    except Exception as e:
        results["providers"].append({
            "source": "CelesTrak",
            "error": str(e)
        })

    try:
        results["providers"].append(_satnogs(target))
    except Exception as e:
        results["providers"].append({
            "source": "SatNOGS",
            "error": str(e)
        })

    try:
        results["providers"].append(_n2yo(target))
    except Exception as e:
        results["providers"].append({
            "source": "N2YO",
            "error": str(e)
        })

    return results
