import dns.resolver

def run(target):
    domain=target.strip().replace("https://","").replace("http://","").split("/")[0]
    out={"module":"dns","target":domain,"records":{}}
    for typ in ["A","AAAA","MX","NS","TXT","CNAME"]:
        try:
            out["records"][typ]=[str(x) for x in dns.resolver.resolve(domain,typ)]
        except Exception:
            out["records"][typ]=[]
    return out
