import requests

COMMON=[
"www","mail","api","dev","test","staging","app","admin",
"portal","blog","shop","cdn","static","vpn","remote"
]

def run(target):
    domain=target.strip().replace("https://","").replace("http://","").split("/")[0]
    found=[]
    for sub in COMMON:
        host=f"{sub}.{domain}"
        try:
            r=requests.get("https://"+host,timeout=3,allow_redirects=False,
                           headers={"User-Agent":"NIPHER/0.1"})
            if r.status_code:
                found.append({"host":host,"status":r.status_code})
        except Exception:
            pass
    return {"module":"subdomain","target":domain,"found":found}
