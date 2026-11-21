#!/usr/bin/env python3
"""
A©tor — Apostille PDF link integrity checker
CASE-MACHERET-1997-2026

Checks all 90 apostille PDF URLs on GitHub Pages.
Exit code 0 = all OK; 1 = failures found.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REGISTRY = "https://arhiv1973b.github.io/apostille-archive-english/"
DEFAULT_BASE = "https://arhiv1973b.github.io/apostille-archive-english/"
UA = "A\u00a9tor-Apostille-Link-Checker/1.0 (+CASE-MACHERET-1997-2026)"


def fetch_text(url: str, timeout: float = 30.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_pdfs(html: str) -> list[str]:
    found = re.findall(r"apostille_[A-Z0-9]+_\d+\.pdf", html, flags=re.I)
    seen: set[str] = set()
    out: list[str] = []
    for name in found:
        key = name.lower()
        if key not in seen:
            seen.add(key)
            out.append(name)
    return out


def check_one(url: str, timeout: float = 20.0) -> dict:
    t0 = time.perf_counter()
    result = {
        "url": url,
        "ok": False,
        "status": None,
        "content_type": None,
        "content_length": None,
        "error": None,
        "ms": None,
    }
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result["status"] = resp.status
            result["content_type"] = resp.headers.get("Content-Type")
            cl = resp.headers.get("Content-Length")
            result["content_length"] = int(cl) if cl and cl.isdigit() else None
            ct = (result["content_type"] or "").lower()
            result["ok"] = (
                resp.status == 200
                and ("pdf" in ct or "octet-stream" in ct or result["content_length"] is not None)
            )
            if result["status"] == 200 and not result["ok"]:
                req2 = urllib.request.Request(
                    url,
                    headers={"User-Agent": UA, "Range": "bytes=0-4"},
                )
                with urllib.request.urlopen(req2, timeout=timeout) as r2:
                    magic = r2.read(5)
                    result["ok"] = magic.startswith(b"%PDF")
                    result["status"] = r2.status if r2.status != 206 else 200
                    result["content_type"] = r2.headers.get("Content-Type") or result["content_type"]
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["error"] = str(e.reason)
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
    result["ms"] = round((time.perf_counter() - t0) * 1000)
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Check apostille PDF download links")
    ap.add_argument("--registry", default=DEFAULT_REGISTRY, help="HTML page with PDF names")
    ap.add_argument("--base", default=DEFAULT_BASE, help="Base URL for PDF files")
    ap.add_argument("--workers", type=int, default=12, help="Parallel HEAD workers")
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--json-out", default="", help="Write full JSON report path")
    ap.add_argument("--list", default="", help="Optional local list of filenames (one per line)")
    args = ap.parse_args()

    base = args.base.rstrip("/") + "/"

    if args.list:
        names = [
            ln.strip()
            for ln in Path(args.list).read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.strip().startswith("#")
        ]
    else:
        print(f"[1/3] Fetching registry: {args.registry}")
        html = fetch_text(args.registry, timeout=args.timeout)
        names = extract_pdfs(html)
        print(f"      Found {len(names)} unique PDF names")

    if not names:
        print("ERROR: no PDF names found", file=sys.stderr)
        return 1

    urls = [base + n if not n.startswith("http") else n for n in names]

    print(f"[2/3] Checking {len(urls)} links ({args.workers} workers)…")
    results: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(check_one, u, args.timeout): u for u in urls}
        for i, fut in enumerate(concurrent.futures.as_completed(futs), 1):
            r = fut.result()
            results.append(r)
            mark = "OK " if r["ok"] else "FAIL"
            name = r["url"].rsplit("/", 1)[-1]
            extra = r["error"] or r["content_type"] or ""
            print(f"  [{i:02d}/{len(urls)}] {mark}  {name}  {r['status']}  {r['ms']}ms  {extra}")

    order = {u: i for i, u in enumerate(urls)}
    results.sort(key=lambda r: order.get(r["url"], 9999))

    ok = [r for r in results if r["ok"]]
    bad = [r for r in results if not r["ok"]]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "registry": args.registry,
        "base": base,
        "total": len(results),
        "ok": len(ok),
        "failed": len(bad),
        "failures": bad,
        "results": results,
    }

    print()
    print("[3/3] Summary")
    print(f"  Total : {len(results)}")
    print(f"  OK    : {len(ok)}")
    print(f"  FAIL  : {len(bad)}")

    if bad:
        print("\n  Failed URLs:")
        for r in bad:
            print(f"    - {r['url']}  status={r['status']}  err={r['error']}")

    out_path = args.json_out or str(
        Path(__file__).resolve().parent / "apostille_link_check_report.json"
    )
    Path(out_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  JSON report: {out_path}")

    md_path = str(Path(out_path).with_suffix(".md"))
    lines = [
        f"# Apostille Link Check Report",
        f"",
        f"- **When:** {report['generated_at']}",
        f"- **Registry:** {args.registry}",
        f"- **Total:** {len(results)}",
        f"- **OK:** {len(ok)}",
        f"- **FAIL:** {len(bad)}",
        f"",
    ]
    if bad:
        lines.append("## Failures")
        for r in bad:
            lines.append(f"- `{r['url']}` — status={r['status']} error={r['error']}")
    else:
        lines.append("## Result")
        lines.append("All apostille PDF links returned HTTP 200 and valid PDF response.")
    Path(md_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Markdown:   {md_path}")

    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
