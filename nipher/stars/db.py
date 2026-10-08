import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[2] / "data" / "stars.db"

STARS = [
    ("Sirius","HIP 32349",-1.46,6.7525,-16.7161,8.60,-1.46),
    ("Canopus","HIP 30438",-0.74,6.3992,-52.6957,310.0,-0.74),
    ("Arcturus","HIP 69673",-0.05,14.2610,19.1824,36.7,-0.05),
    ("Vega","HIP 91262",0.03,18.6156,38.7837,25.0,0.03),
    ("Capella","HIP 24608",0.08,5.2782,45.9980,42.9,0.08),
    ("Rigel","HIP 24436",0.13,5.2423,-8.2016,860.0,0.13),
    ("Procyon","HIP 37279",0.34,7.6550,5.2250,11.46,0.34),
    ("Betelgeuse","HIP 27989",0.42,5.9195,7.4071,642.5,0.42),
    ("Achernar","HIP 7588",0.46,1.6286,-57.2368,139.0,0.46),
    ("Altair","HIP 97649",0.77,19.8464,8.8683,16.73,0.77),
    ("Aldebaran","HIP 21421",0.85,4.5987,16.5093,65.23,0.85),
    ("Antares","HIP 80763",0.96,16.4901,-26.4319,550.0,0.96),
    ("Spica","HIP 65474",0.98,13.4199,-11.1614,250.0,0.98),
    ("Pollux","HIP 37826",1.14,7.7553,28.0262,33.78,1.14),
    ("Deneb","HIP 102098",1.25,20.6905,45.2803,2615.0,1.25),
    ("Regulus","HIP 49669",1.40,10.1395,11.9672,79.3,1.40),
    ("Polaris","HIP 11767",1.98,2.5303,89.2641,433.8,1.98),
    ("VY Canis Majoris","HIP 35793",6.5,7.3829,-25.7683,3900.0,6.5),
]

def init():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS stars (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            catalog_id TEXT,
            magnitude REAL,
            ra_deg REAL,
            dec_deg REAL,
            distance_ly REAL,
            visual_magnitude REAL
        )
    """)
    con.executemany("""
        INSERT OR IGNORE INTO stars
        (name,catalog_id,magnitude,ra_deg,dec_deg,distance_ly,visual_magnitude)
        VALUES (?,?,?,?,?,?,?)
    """, STARS)
    con.commit()
    con.close()

def all_stars():
    init()
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(
        "SELECT * FROM stars ORDER BY magnitude ASC"
    )]
    con.close()
    return rows

def search(q):
    init()
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(
        "SELECT * FROM stars WHERE name LIKE ? OR catalog_id LIKE ? ORDER BY magnitude ASC LIMIT 20",
        (f"%{q}%", f"%{q}%")
    )]
    con.close()
    return rows
