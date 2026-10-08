from pathlib import Path
import os

HOME = Path(os.environ.get("NIPHER_HOME", Path.home() / "projects" / "nipher"))
DATA = HOME / "data"
REPORTS = HOME / "reports"
DOWNLOADS = HOME / "downloads"
CACHE = HOME / "cache"

for path in (DATA, REPORTS, DOWNLOADS, CACHE):
    path.mkdir(parents=True, exist_ok=True)
