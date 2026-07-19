#!/usr/bin/env python3
"""Generate a local MP3 with Doubao TTS 2.0 without exposing credentials."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ENDPOINT = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
RESOURCE_ID = "seed-tts-2.0"
DEFAULT_SPEAKER = "zh_male_yuanboxiaoshu_uranus_bigtts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 spoken-script text file")
    parser.add_argument("--output", required=True, type=Path, help="destination MP3 path")
    parser.add_argument("--speaker", default=DEFAULT_SPEAKER, help="Doubao TTS 2.0 speaker ID")
    return parser.parse_args()


def load_api_key() -> str | None:
    for name in ("DOUBAO_TTS_API_KEY", "VOLCENGINE_API_KEY"):
        if value := os.environ.get(name):
            return value
    return None


def decode_events(raw: str) -> tuple[list[dict], list[bytes]]:
    decoder = json.JSONDecoder()
    index = 0
    events: list[dict] = []
    chunks: list[bytes] = []
    while index < len(raw):
        while index < len(raw) and raw[index].isspace():
            index += 1
        if index >= len(raw):
            break
        event, index = decoder.raw_decode(raw, index)
        if not isinstance(event, dict):
            raise ValueError("TTS returned an unexpected event")
        events.append(event)
        encoded = event.get("data") or event.get("audio")
        if encoded:
            chunks.append(base64.b64decode(encoded))
    return events, chunks


def main() -> int:
    args = parse_args()
    api_key = load_api_key()
    if not api_key:
        print("Set DOUBAO_TTS_API_KEY or VOLCENGINE_API_KEY.", file=sys.stderr)
        return 2

    text = args.input.read_text(encoding="utf-8").strip()
    if not text:
        print("Spoken script is empty.", file=sys.stderr)
        return 2

    payload = {
        "user": {"uid": "ai-learning-daily-brief"},
        "req_params": {
            "text": text,
            "speaker": args.speaker,
            "audio_params": {"format": "mp3", "sample_rate": 24000},
        },
    }
    request = Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Api-Key": api_key,
            "X-Api-Resource-Id": RESOURCE_ID,
            "X-Api-Request-Id": str(uuid.uuid4()),
        },
    )
    try:
        with urlopen(request, timeout=120) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as error:
        message = error.headers.get("X-Api-Message", "")
        log_id = error.headers.get("X-Tt-Logid", "")
        print(f"Doubao TTS failed: HTTP {error.code}; {message}; log_id={log_id}", file=sys.stderr)
        return 1
    except URLError as error:
        print(f"Doubao TTS connection failed: {error.reason}", file=sys.stderr)
        return 1

    try:
        events, chunks = decode_events(raw)
    except (ValueError, json.JSONDecodeError, base64.binascii.Error) as error:
        print(f"Doubao TTS response parsing failed: {error}", file=sys.stderr)
        return 1

    errors = [event for event in events if event.get("code") not in (0, 20000000)]
    if errors or not chunks:
        message = errors[-1].get("message", "no audio returned") if errors else "no audio returned"
        print(f"Doubao TTS failed: {message}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(b"".join(chunks))
    print(json.dumps({"output": str(args.output.resolve()), "characters": len(text), "audio_chunks": len(chunks)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
