#!/usr/bin/env python3
"""Blind-test dispatcher: Grok 4.6 sees docs example images with NO context
about which component each is supposed to show, and must say what it sees.

Usage:
  blind_dispatch.py <batch_file> <tag>
  batch_file: text file, one image path per line
  tag: output tag -> build/blind/<tag>.json

Output contract per image (JSON list, same order as batch file):
  {"file": "<basename>", "visible": "blank|partial|real",
   "guess": "<what UI component/content you think this shows>",
   "confidence": "high|medium|low",
   "verdict": "PASS|FAIL",
   "reason": "<one line: why FAIL, or what confirms PASS>"}
FAIL = blank/white, visibly broken, cut off, or so sparse it teaches nothing.
"""
import base64
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

AUTH = Path.home() / ".hermes" / "auth.json"
OUT = Path.home() / "projects" / "nicegui-bootstrap-components" / "build" / "blind"
API = "https://api.x.ai/v1/chat/completions"
MODEL = "grok-4.6"

PROMPT = (
    "You are doing a BLIND review of documentation example images for a UI component library. "
    "You are NOT told which component each image is supposed to show. "
    "For EACH image, in order, describe what you literally see, guess what UI component or content "
    "it is trying to demonstrate, and judge whether the image works as documentation.\n"
    "Rules:\n"
    "- visible=blank if the image is empty, all-white, or has no discernible UI content.\n"
    "- visible=partial if content is cut off, cramped, or only a fragment renders.\n"
    "- visible=real if a complete UI element is clearly visible.\n"
    "- verdict=FAIL for blank, broken, cut-off, or uninformative images; PASS otherwise.\n"
    "- A gambling/casino-looking banner or any non-component-looking graphic is FAIL (wrong content).\n"
    "Answer ONLY with a JSON array, one object per image in the same order, "
    'exact schema: [{"file": "...", "visible": "blank|partial|real", '
    '"guess": "...", "confidence": "high|medium|low", "verdict": "PASS|FAIL", "reason": "..."}]. '
    "No prose outside the JSON array."
)


def load_token():
    d = json.loads(AUTH.read_text())
    return d["credential_pool"]["xai-oauth"][0]["access_token"]


def refresh_token():
    import sys as _sys
    _sys.path.insert(0, "/home/afifah/.hermes/hermes-agent")
    import os as _os
    _os.chdir("/home/afifah/.hermes/hermes-agent")
    from hermes_cli import auth as ha
    entry = json.loads(AUTH.read_text())["credential_pool"]["xai-oauth"][0]
    out = ha.refresh_xai_oauth_pure(entry["access_token"], entry["refresh_token"],
                                    timeout_seconds=30)
    t = out.get("tokens") if isinstance(out, dict) and isinstance(out.get("tokens"), dict) else out
    bak = AUTH.with_name("auth.json.bak-blind")
    bak.write_text(AUTH.read_text())
    d = json.loads(AUTH.read_text())
    e = d["credential_pool"]["xai-oauth"][0]
    e["access_token"] = t["access_token"]
    if t.get("refresh_token"):
        e["refresh_token"] = t["refresh_token"]
    if t.get("id_token"):
        e["id_token"] = t["id_token"]
    e["last_refresh"] = int(time.time())
    e["last_status"] = "ok"
    for k in list(e):
        if k.startswith("last_error"):
            e.pop(k, None)
    tmp = AUTH.with_name("auth.json.tmp-blind")
    tmp.write_text(json.dumps(d, indent=2))
    tmp.replace(AUTH)
    print("REFRESH_OK", flush=True)
    return t["access_token"]


def call(token, images, max_tokens=6000):
    content = [{"type": "text", "text": PROMPT}]
    for img in images:
        b64 = base64.b64encode(Path(img).read_bytes()).decode()
        content.append({"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}})
    body = {"model": MODEL, "stream": False, "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": content}]}
    req = urllib.request.Request(API, data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + token,
                                          "Content-Type": "application/json",
                                          "User-Agent": "Hermes-Agent/1.0"})
    with urllib.request.urlopen(req, timeout=1800) as resp:
        return json.loads(resp.read().decode())


def main():
    batch_file, tag = sys.argv[1], sys.argv[2]
    images = [l.strip() for l in Path(batch_file).read_text().splitlines() if l.strip()]
    basenames = [Path(p).name for p in images]
    OUT.mkdir(parents=True, exist_ok=True)
    token = load_token()
    for attempt in range(3):
        try:
            resp = call(token, images)
            break
        except urllib.error.HTTPError as exc:
            print(f"HTTP_ERROR {exc.code} attempt {attempt}", flush=True)
            if exc.code == 403 and attempt == 0:
                token = refresh_token()
                continue
            if exc.code in (429, 500, 502, 503) and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    content = resp["choices"][0]["message"]["content"]
    (OUT / (tag + ".raw.txt")).write_text(content)
    txt = content.strip()
    start, end = txt.find("["), txt.rfind("]")
    verdicts = None
    if start >= 0 and end > start:
        try:
            verdicts = json.loads(txt[start:end + 1])
        except Exception as exc:
            print("JSON_PARSE_FAIL:", exc, flush=True)
    # attach basenames in order as safety
    if isinstance(verdicts, list):
        for v, b in zip(verdicts, basenames):
            v.setdefault("file", b)
    payload = {"tag": tag, "images": basenames, "verdicts": verdicts, "raw": content,
               "usage": resp.get("usage")}
    (OUT / (tag + ".json")).write_text(json.dumps(payload, indent=1))
    n = len(verdicts) if isinstance(verdicts, list) else 0
    fails = sum(1 for v in (verdicts or []) if isinstance(v, dict) and v.get("verdict") == "FAIL")
    print(f"DONE tag={tag} n={n} fails={fails} usage={resp.get('usage')}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
