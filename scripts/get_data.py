"""Download FALCON datasets from DANDI into data/<task>/{held_in_calib,held_out_calib,minival}/
and verify them against data_manifest.json (SHA-256 per file).

Usage: python scripts/get_data.py h1 m1 [h2 m2] [--write-manifest]
Sizes: h1 ~0.1 GB, m1 ~0.3 GB, h2 ~1.2 GB, m2 ~15.9 GB.

Versions: M1 is pinned to the published DANDI version below. H1 (000954) has no published version
(only `draft`, as of Nov 2026), so the manifest's checksums are the pin: a changed file fails loudly.
"""
import argparse
import hashlib
import json
import pathlib
import urllib.request

DANDISETS = {"h1": ("000954", "draft"), "m1": ("000941", "0.241029.1405"),
             "h2": ("000950", "draft"), "m2": ("000953", "draft")}
API = "https://api.dandiarchive.org/api"
ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MANIFEST = ROOT / "data_manifest.json"


def split_of(path):
    for key, name in (("held-in-calib", "held_in_calib"), ("held-out-calib", "held_out_calib"), ("minival", "minival")):
        if key in path:
            return name
    return None


def list_assets(dandiset, version):
    url = f"{API}/dandisets/{dandiset}/versions/{version}/assets/?page_size=400"
    out = []
    while url:
        with urllib.request.urlopen(url) as r:
            page = json.load(r)
        out += page["results"]
        url = page.get("next")
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tasks", nargs="+", choices=sorted(DANDISETS))
    ap.add_argument("--write-manifest", action="store_true", help="record checksums of the downloaded files")
    a = ap.parse_args()
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    bad = []
    for task in a.tasks:
        dandiset, version = DANDISETS[task]
        assets = [x for x in list_assets(dandiset, version) if split_of(x["path"])]
        print(f"{task}: DANDI {dandiset}@{version}, {len(assets)} files, {sum(x['size'] for x in assets) / 1e9:.2f} GB")
        entries = {}
        for x in assets:
            rel = f"{task}/{split_of(x['path'])}/{pathlib.Path(x['path']).name}"
            dest = DATA / rel
            if not (dest.exists() and dest.stat().st_size == x["size"]):
                dest.parent.mkdir(parents=True, exist_ok=True)
                urllib.request.urlretrieve(f"{API}/assets/{x['asset_id']}/download/", dest)
                print("   downloaded", rel)
            digest = sha256(dest)
            entries[rel] = {"asset_id": x["asset_id"], "size": x["size"], "sha256": digest}
            want = manifest.get(task, {}).get("files", {}).get(rel, {}).get("sha256")
            if want and want != digest:
                bad.append(rel)
        if a.write_manifest:
            manifest[task] = {"dandiset": dandiset, "version": version, "files": dict(sorted(entries.items()))}
    if a.write_manifest:
        MANIFEST.write_text(json.dumps(manifest, indent=1) + "\n")
        print("wrote", MANIFEST.name)
    if bad:
        raise SystemExit(f"checksum mismatch vs data_manifest.json: {bad}")
    print("checksums OK" if manifest else "no manifest to verify against")


if __name__ == "__main__":
    main()
