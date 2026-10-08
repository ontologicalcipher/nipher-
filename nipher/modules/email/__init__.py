import dns.resolver

def run(target):
    domain=target.strip().lower().split("@")[-1]
    result={"module":"email","target":target,"domain":domain}
    for typ,name in [("MX","mx"),("TXT","txt")]:
        try:
            result[name]=[str(x) for x in dns.resolver.resolve(domain,typ)]
        except Exception:
            result[name]=[]
    try:
        txt=result["txt"]
        result["spf"]=[x for x in txt if "v=spf1" in x.lower()]
    except Exception:
        result["spf"]=[]
    try:
        result["dmarc"]=[str(x) for x in dns.resolver.resolve("_dmarc."+domain,"TXT")]
    except Exception:
        result["dmarc"]=[]
    return result
