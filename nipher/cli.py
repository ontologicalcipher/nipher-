import argparse
import json

from nipher.core.engine import Engine

def main():
    parser = argparse.ArgumentParser(
        prog="nipher",
        description="NIPHER — Public OSINT & GEOINT Toolkit",
    )

    parser.add_argument("--version", action="version", version="NIPHER 0.1.0")

    sub = parser.add_subparsers(dest="module", required=True)

    for name in Engine.MODULES:
        p = sub.add_parser(name)
        p.add_argument("target")
        p.add_argument("--json", action="store_true")

    args = parser.parse_args()

    try:
        result = Engine().run(args.module, args.target)

        if hasattr(result, "to_dict"):
            result = result.to_dict()

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(json.dumps(result, indent=2, default=str))

    except Exception as exc:
        error = {
            "module": args.module,
            "target": args.target,
            "success": False,
            "error": str(exc),
        }
        print(json.dumps(error, indent=2))
        raise SystemExit(1)
