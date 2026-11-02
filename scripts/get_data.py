"""Download FALCON datasets from DANDI into data/<task>/{held_in_calib,held_out_calib,minival}/.

Usage: python scripts/get_data.py h1 m1 [h2 m2] [--dry-run]
Sizes (DANDI draft, Nov 2026): h1 ~0.1 GB, m1 ~0.3 GB, h2 ~1.2 GB, m2 ~15.9 GB.
"""
import argparse
import json
import pathlib
import urllib.request

DANDISETS = {"h1": "000954", "m1": "000941", "h2": "000950", "m2": "000953"}
API = "https://api.dandiarchive.org/api"
ROOT = pathlib.Path(__file__).resolve().parents[1] / "data"


def split_of(path):
    for key, name in (("held-in-calib", "held_in_calib"), ("held-out-calib", "held_out_calib"), ("minival", "minival")):
        if key in path:
            return name
    return None


def list_assets(dandiset):
    url = f"{API}/dandisets/{dandiset}/versions/draft/assets/?page_size=400"
    out = []
    while url:
        with urllib.request.urlopen(url) as r:
            page = json.load(r)
        out += page["results"]
        url = page.get("next")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tasks", nargs="+", choices=sorted(DANDISETS))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    for task in a.tasks:
        assets = [x for x in list_assets(DANDISETS[task]) if split_of(x["path"])]
        print(f"{task}: {len(assets)} files, {sum(x['size'] for x in assets) / 1e9:.2f} GB")
        for x in assets:
            dest = ROOT / task / split_of(x["path"]) / pathlib.Path(x["path"]).name
            if a.dry_run or (dest.exists() and dest.stat().st_size == x["size"]):
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(f"{API}/assets/{x['asset_id']}/download/", dest)
            print("  ", dest.relative_to(ROOT))


if __name__ == "__main__":
    main()
