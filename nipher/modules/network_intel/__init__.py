import socket, requests, ipaddress

def run(target):
    target=target.strip()
    try:
        ip=socket.gethostbyname(target)
    except Exception:
        ip=target
    result={"module":"network","target":target,"ip":ip}
    try:
        ipaddress.ip_address(ip)
        result["reverse_dns"]=socket.gethostbyaddr(ip)[0]
    except Exception:
        result["reverse_dns"]=None
    try:
        r=requests.get("https://ipwho.is/"+ip,timeout=10)
        if r.ok:
            d=r.json()
            result["location"]={
                "country":d.get("country"),
                "region":d.get("region"),
                "city":d.get("city"),
                "latitude":d.get("latitude"),
                "longitude":d.get("longitude")
            }
            result["asn"]=d.get("connection",{}).get("asn")
            result["isp"]=d.get("connection",{}).get("isp")
            result["org"]=d.get("connection",{}).get("org")
        else:
            result["error"]="IP information service returned "+str(r.status_code)
    except Exception as e:
        result["error"]=str(e)
    return result
