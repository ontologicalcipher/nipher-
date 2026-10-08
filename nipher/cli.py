import argparse
import json

from nipher.core.engine import Engine


def main():
    parser = argparse.ArgumentParser(
        prog="nipher",
        description="NIPHER — Public OSINT & GEOINT Toolkit",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="NIPHER 0.1.0",
    )

    sub = parser.add_subparsers(dest="module", required=True)

    for name in Engine.MODULES:
        p = sub.add_parser(name)
        p.add_argument("target")
        p.add_argument("--json", action="store_true")

        if name == "satellite":
            p.add_argument("--lat", type=float)
            p.add_argument("--lon", type=float)
            p.add_argument("--hours", type=float, default=24)
            p.add_argument("--min-elevation", type=float, default=10)
            p.add_argument("--passes", action="store_true")

    args = parser.parse_args()

    try:
        kwargs = {}

        if args.module == "satellite" and args.passes:
            if args.lat is None or args.lon is None:
                raise ValueError(
                    "--passes requires both --lat and --lon"
                )

            from nipher.modules.satellite import (
                _get_satellite,
                passes,
            )

            target = "25544" if args.target.upper() == "ISS" else args.target

            if not target.isdigit():
                raise ValueError(
                    "Satellite must be a NORAD catalog ID or ISS"
                )

            item = _get_satellite(target)

            result = {
                "module": "satellite",
                "target": args.target,
                "source": "CelesTrak",
                "observer": {
                    "latitude_deg": args.lat,
                    "longitude_deg": args.lon,
                },
                "prediction": {
                    "hours": args.hours,
                    "minimum_elevation_deg": args.min_elevation,
                },
                "passes": passes(
                    item,
                    args.lat,
                    args.lon,
                    hours=args.hours,
                    min_elevation=args.min_elevation,
                ),
            }
        else:
            result = Engine().run(
                args.module,
                args.target,
                **kwargs,
            )

        if hasattr(result, "to_dict"):
            result = result.to_dict()

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


if __name__ == "__main__":
    main()
