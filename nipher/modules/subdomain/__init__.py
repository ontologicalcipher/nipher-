import requests


def run(target, **kwargs):
    target = target.strip().lower()

    if not target:
        raise ValueError("Domain cannot be empty")

    if target.startswith("http://") or target.startswith("https://"):
        target = target.split("://", 1)[1].split("/", 1)[0]

    try:
        url = f"https://crt.sh/?q=%25.{target}&output=json"
        response = requests.get(url, timeout=8)
        response.raise_for_status()

        names = set()

        for item in response.json():
            for name in item.get("name_value", "").splitlines():
                name = name.strip().lower()
                if name.startswith("*."):
                    name = name[2:]
                if name == target or name.endswith("." + target):
                    names.add(name)

        return {
            "success": True,
            "module": "subdomain",
            "target": target,
            "count": len(names),
            "subdomains": sorted(names),
            "source": "crt.sh",
        }

    except Exception as e:
        return {
            "success": False,
            "module": "subdomain",
            "target": target,
            "error": str(e),
        }
