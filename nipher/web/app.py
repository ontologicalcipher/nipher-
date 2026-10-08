from flask import Flask, render_template, request, jsonify
import importlib

app = Flask(__name__)

MODULES = [
    ("domain","Domain OSINT","DNS / HTTP / IP"),
    ("dns","DNS Lookup","A / AAAA / MX / NS / TXT"),
    ("whois","WHOIS","Domain registration"),
    ("ssl","SSL / TLS","Certificate"),
    ("subdomain","Subdomains","Passive discovery"),
    ("ip","IP Intelligence","IP / ASN / ISP"),
    ("country","Country Info","Country information"),
    ("pincode","Pincode","Pincode information"),
    ("ifsc","IFSC","Bank branch information"),
    ("number","Number Info","Phone number"),
    ("email","Email Domain","MX / SPF / DMARC"),
    ("username","Username","Public profiles"),
    ("github","GitHub","Repository search"),
    ("youtube_api","YouTube","Public video information"),
    ("metadata","Metadata","EXIF / file metadata"),
    ("hash","Hash Analyzer","MD5 / SHA1 / SHA256"),
    ("url","URL Analyzer","HTTP / redirects / headers"),
    ("geoint","GEOINT","Coordinates / places"),
    ("satellite","Satellite","Orbital tracking"),
    ("satellite_intel","Satellite Intelligence","Live multi-source satellite data"),
    ("satellite_sources","Satellite OSINT","Tracking / orbital / imagery sources"),
    ("pan","PAN Validator","Format validation"),
    ("gst","GST Info","GST verification"),
    ("report","Reports","Combined report"),
]

MODULE_MAP = {x[0]: x[1] for x in MODULES}

@app.route("/")
def index():
    return render_template("index.html", modules=MODULES)

@app.post("/api/run")
def run_module():
    data = request.get_json(silent=True) or {}
    module = str(data.get("module", "")).strip().lower()
    target = str(data.get("target", "")).strip()

    if module not in MODULE_MAP:
        return jsonify({"error": "Unknown module", "module": module}), 400

    if not target:
        return jsonify({"error": "Target is required"}), 400

    try:
        mod = importlib.import_module(f"nipher.modules.{module}")
        if not hasattr(mod, "run"):
            return jsonify({"error": f"{module} has no run() function"}), 500

        result = mod.run(target)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "module": module,
            "target": target
        }), 500

@app.get("/api/modules")
def modules():
    return jsonify([
        {"id": i, "name": n, "description": d}
        for i, n, d in MODULES
    ])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
