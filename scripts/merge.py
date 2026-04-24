#!/usr/bin/env python3
"""
merge.py — org-*.yaml を読み込み master.yaml を生成する
使用方法: python scripts/merge.py
"""
import glob
import yaml
from pathlib import Path

HOLIDAYS = [{"date": "2026-04-29", "name": "昭和の日"}]
OUTPUT = Path("master.yaml")
SCHEDULES_DIR = Path("schedules")


def load_org_files():
    entries = []
    for path in sorted(SCHEDULES_DIR.glob("org-*.yaml")):
        with open(path) as f:
            data = yaml.safe_load(f)
        org_id = data.get("org", path.stem)
        for s in data.get("schedules", []):
            entry = {
                "id": f"{s['start_date']}-{s['course']}-{org_id}",
                "org": org_id,
                "course": s["course"],
                "version": s.get("version", ""),
                "duration_days": s["duration_days"],
                "start_date": s["start_date"],
                "end_date": s["end_date"],
                "instructor": s.get("instructor", ""),
                "status": s.get("status", "unassigned"),
                "notes": s.get("notes", ""),
            }
            entries.append(entry)
    return sorted(entries, key=lambda x: (x["start_date"], x["org"]))


def main():
    schedules = load_org_files()
    master = {
        "month": "2026-04",
        "holidays": [{"date": h["date"]} for h in HOLIDAYS],
        "schedules": schedules,
    }
    with open(OUTPUT, "w") as f:
        yaml.dump(master, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    print(f"✅ {OUTPUT} を生成しました ({len(schedules)} 件)")


if __name__ == "__main__":
    main()
