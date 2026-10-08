import socket, requests
from urllib.parse import urlparse

def run(target):
    domain=target.strip().replace("https://","").replace("http://","").split("/")[0]
    result={"module":"domain","target":domain}
    try:
        result["ip_addresses"]=sorted(set(socket.gethostbyname_ex(domain)[2]))
    except Exception as e:
        result["ip_error"]=str(e)
    try:
        r=requests.get("https://"+domain,timeout=10,allow_redirects=True,
                       headers={"User-Agent":"NIPHER/0.1"})
        result["http"]={"status":r.status_code,"final_url":r.url,
                         "server":r.headers.get("server"),
                         "content_type":r.headers.get("content-type")}
        result["title"]=r.text.split("<title>",1)[1].split("</title>",1)[0].strip() if "<title>" in r.text.lower() else None
    except Exception as e:
        result["http_error"]=str(e)
    return result
