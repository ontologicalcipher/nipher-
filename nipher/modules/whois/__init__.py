import whois

def run(target):
    domain=target.strip().replace("https://","").replace("http://","").split("/")[0]
    try:
        w=whois.whois(domain)
        return {
            "module":"whois","target":domain,
            "domain_name":str(w.domain_name),
            "registrar":str(w.registrar),
            "creation_date":str(w.creation_date),
            "expiration_date":str(w.expiration_date),
            "name_servers":[str(x) for x in (w.name_servers or [])]
        }
    except Exception as e:
        return {"module":"whois","target":domain,"error":str(e)}
