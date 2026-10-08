from datetime import datetime, timezone
from math import sin, cos, sqrt, atan2, asin, pi, radians, degrees
import requests

from sgp4.api import Satrec, WGS72

CELESTRAK = "https://celestrak.org/NORAD/elements/gp.php"
WGS84_A = 6378.137
WGS84_F = 1 / 298.257223563
WGS84_E2 = WGS84_F * (2 - WGS84_F)


def _get_satellite(norad_id):
    r = requests.get(
        CELESTRAK,
        params={"CATNR": str(norad_id), "FORMAT": "JSON"},
        headers={"User-Agent": "NIPHER/0.1"},
        timeout=20,
    )
    r.raise_for_status()

    data = r.json()

    if not data:
        raise ValueError(f"Satellite not found: {norad_id}")

    return data[0]


def _julian_date(dt):
    y = dt.year
    m = dt.month

    if m <= 2:
        y -= 1
        m += 12

    a = y // 100
    b = 2 - a + a // 4

    jd = (
        int(365.25 * (y + 4716))
        + int(30.6001 * (m + 1))
        + dt.day
        + b
        - 1524.5
    )

    fraction = (
        dt.hour
        + dt.minute / 60
        + dt.second / 3600
        + dt.microsecond / 3_600_000_000
    ) / 24

    return jd + fraction


def _gmst(jd):
    t = (jd - 2451545.0) / 36525.0

    value = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * t * t
        - (t * t * t) / 38710000.0
    )

    return radians(value % 360.0)


def _build_satellite(item):
    sat = Satrec()

    epoch = datetime.fromisoformat(item["EPOCH"]).replace(
        tzinfo=timezone.utc
    )

    epoch_days = (
        epoch - datetime(1949, 12, 31, tzinfo=timezone.utc)
    ).total_seconds() / 86400.0

    # CelesTrak: rev/day² -> rad/min²
    ndot = (
        float(item["MEAN_MOTION_DOT"])
        * 2.0 * pi
        / (1440.0 ** 2)
    )

    # CelesTrak: rev/day³ -> rad/min³
    nddot = (
        float(item["MEAN_MOTION_DDOT"])
        * 2.0 * pi
        / (1440.0 ** 3)
    )

    # CelesTrak: rev/day -> rad/min
    mean_motion = (
        float(item["MEAN_MOTION"])
        * 2.0 * pi
        / 1440.0
    )

    sat.sgp4init(
        WGS72,
        "i",
        int(item["NORAD_CAT_ID"]),
        epoch_days,
        float(item["BSTAR"]),
        ndot,
        nddot,
        float(item["ECCENTRICITY"]),
        radians(float(item["ARG_OF_PERICENTER"])),
        radians(float(item["INCLINATION"])),
        radians(float(item["MEAN_ANOMALY"])),
        mean_motion,
        radians(float(item["RA_OF_ASC_NODE"])),
    )

    return sat


def _teme_to_geodetic(position, jd):
    x, y, z = position

    # TEME -> Earth-fixed coordinates using GMST.
    theta = _gmst(jd)

    x_ecef = cos(theta) * x + sin(theta) * y
    y_ecef = -sin(theta) * x + cos(theta) * y
    z_ecef = z

    longitude = atan2(y_ecef, x_ecef)

    # Iterative WGS-84 geodetic latitude/altitude.
    p = sqrt(x_ecef * x_ecef + y_ecef * y_ecef)

    latitude = atan2(
        z_ecef,
        p * (1 - WGS84_E2),
    )

    for _ in range(10):
        sin_lat = sin(latitude)
        n = WGS84_A / sqrt(
            1 - WGS84_E2 * sin_lat * sin_lat
        )
        altitude = p / cos(latitude) - n

        latitude = atan2(
            z_ecef,
            p * (
                1
                - WGS84_E2 * n / (n + altitude)
            ),
        )

    sin_lat = sin(latitude)
    n = WGS84_A / sqrt(
        1 - WGS84_E2 * sin_lat * sin_lat
    )

    altitude = p / cos(latitude) - n

    return {
        "latitude_deg": round(degrees(latitude), 6),
        "longitude_deg": round(degrees(longitude), 6),
        "altitude_km": round(altitude, 3),
        "position_ecef_km": [
            round(x_ecef, 6),
            round(y_ecef, 6),
            round(z_ecef, 6),
        ],
    }


def _position(item):
    sat = _build_satellite(item)
    now = datetime.now(timezone.utc)

    jd = _julian_date(now)
    jd_int = int(jd)
    jd_fraction = jd - jd_int

    error, position, velocity = sat.sgp4(
        jd_int,
        jd_fraction,
    )

    if error != 0:
        raise RuntimeError(
            f"SGP4 propagation error: {error}"
        )

    geo = _teme_to_geodetic(position, jd)

    return {
        "timestamp_utc": now.isoformat(),
        **geo,
        "position_teme_km": [
            round(v, 6) for v in position
        ],
        "velocity_teme_km_s": [
            round(v, 6) for v in velocity
        ],
    }


def run(target, **kwargs):
    target = target.strip()

    if target.upper() == "ISS":
        target = "25544"

    if not target.isdigit():
        raise ValueError(
            "Use a NORAD catalog ID, for example: 25544"
        )

    item = _get_satellite(target)

    return {
        "source": "CelesTrak",
        "name": item["OBJECT_NAME"],
        "norad_cat_id": item["NORAD_CAT_ID"],
        "object_id": item["OBJECT_ID"],
        "epoch": item["EPOCH"],
        "orbital_elements": {
            "mean_motion_rev_day": item["MEAN_MOTION"],
            "eccentricity": item["ECCENTRICITY"],
            "inclination_deg": item["INCLINATION"],
            "raan_deg": item["RA_OF_ASC_NODE"],
            "arg_perigee_deg": item["ARG_OF_PERICENTER"],
            "mean_anomaly_deg": item["MEAN_ANOMALY"],
            "bstar": item["BSTAR"],
        },
        "position": _position(item),
    }
