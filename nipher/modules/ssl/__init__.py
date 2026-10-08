import socket
import ssl


def run(target, **kwargs):
    target = target.strip().lower()

    if not target:
        raise ValueError("Domain cannot be empty")

    try:
        context = ssl.create_default_context()

        with socket.create_connection((target, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()

                return {
                    "success": True,
                    "module": "ssl",
                    "target": target,
                    "tls_version": ssock.version(),
                    "cipher": ssock.cipher()[0],
                    "issuer": dict(x[0] for x in cert.get("issuer", [])),
                    "subject": dict(x[0] for x in cert.get("subject", [])),
                    "valid_from": cert.get("notBefore"),
                    "valid_until": cert.get("notAfter"),
                    "san": [
                        value
                        for kind, value in cert.get("subjectAltName", [])
                        if kind == "DNS"
                    ],
                }

    except Exception as e:
        return {
            "success": False,
            "module": "ssl",
            "target": target,
            "error": str(e),
        }
