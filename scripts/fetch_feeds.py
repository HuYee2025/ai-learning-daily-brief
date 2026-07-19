#!/usr/bin/env python3
"""Download the public follow-builders feeds with freshness metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen


BASE_URL = "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main"
FEEDS = {
    "x": ("feed-x.json", "x"),
    "podcasts": ("feed-podcasts.json", "podcasts"),
    "blogs": ("feed-blogs.json", "blogs"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict[str, object]] = {}

    for name, (filename, key) in FEEDS.items():
        request = Request(f"{BASE_URL}/{filename}", headers={"User-Agent": "ai-learning-daily-brief"})
        with urlopen(request, timeout=args.timeout) as response:
            data = json.load(response)
        if not isinstance(data, dict) or not isinstance(data.get(key), list):
            raise ValueError(f"Unexpected schema in {filename}")
        destination = args.output_dir / filename
        destination.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary[name] = {
            "path": str(destination.resolve()),
            "generatedAt": data.get("generatedAt"),
            "items": len(data[key]),
        }

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
