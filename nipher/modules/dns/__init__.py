import socket

def run(target, **kwargs):
    target = target.strip().lower()

    if not target:
        raise ValueError("Domain cannot be empty")

    try:
        infos = socket.getaddrinfo(target, None)
        ips = sorted({item[4][0] for item in infos})

        return {
            "success": True,
            "module": "dns",
            "target": target,
            "addresses": ips,
        }

    except socket.gaierror as e:
        return {
            "success": False,
            "module": "dns",
            "target": target,
            "error": str(e),
        }
