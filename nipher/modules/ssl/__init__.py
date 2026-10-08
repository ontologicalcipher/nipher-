import socket,ssl

def run(target):
    host=target.strip().replace("https://","").replace("http://","").split("/")[0]
    ctx=ssl.create_default_context()
    try:
        with socket.create_connection((host,443),timeout=10) as sock:
            with ctx.wrap_socket(sock,server_hostname=host) as s:
                cert=s.getpeercert()
                return {
                    "module":"ssl","target":host,
                    "version":s.version(),
                    "cipher":s.cipher(),
                    "subject":cert.get("subject"),
                    "issuer":cert.get("issuer"),
                    "valid_from":cert.get("notBefore"),
                    "valid_until":cert.get("notAfter"),
                    "san":[x[1] for x in cert.get("subjectAltName",[])]
                }
    except Exception as e:
        return {"module":"ssl","target":host,"error":str(e)}
