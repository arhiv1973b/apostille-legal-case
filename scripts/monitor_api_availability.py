#!/usr/bin/env python3
"""
A©tor — API / endpoint availability monitor
CASE-MACHERET-1997-2026

Monitors official Moldova apostille services and A©tor archive endpoints.
Exit 0 = all critical OK; 1 = one or more critical failures.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36 "
    "A©tor-API-Monitor/1.2"
)

ENDPOINTS = [
    {
        "id": "apostila.gov.md",
        "url": "https://apostila.gov.md/",
        "critical": True,
        "group": "official",
        "note": "Primary e-apostille portal (historically SSL/connection issues)",
    },
    {
        "id": "www.apostila.gov.md",
        "url": "https://www.apostila.gov.md/",
        "critical": True,
        "group": "official",
        "note": "www variant of apostila portal",
    },
    {
        "id": "eservicii.gov.md/mj/arij",
        "url": "https://eservicii.gov.md/mj/arij/",
        "critical": True,
        "group": "official",
        "note": "ARIJ verification path (codes ARIJ\u2026)",
    },
    {
        "id": "servicii.gov.md",
        "url": "https://servicii.gov.md/",
        "critical": False,
        "group": "official",
        "note": "Government services portal",
    },
    {
        "id": "mcabinet.gov.md",
        "url": "https://mcabinet.gov.md/",
        "critical": False,
        "group": "official",
        "note": "Citizen cabinet (download e-apostille)",
    },
    {
        "id": "justice.gov.md",
        "url": "https://www.justice.gov.md/",
        "critical": False,
        "group": "official",
        "note": "Ministry of Justice",
    },
    {
        "id": "archive-english",
        "url": "https://arhiv1973b.github.io/apostille-archive-english/",
        "critical": True,
        "group": "actor",
        "note": "90-apostille registry + PDF host",
    },
    {
        "id": "legal-case",
        "url": "https://arhiv1973b.github.io/apostille-legal-case/",
        "critical": True,
        "group": "actor",
        "note": "CASE-MACHERET evidence vault",
    },
    {
        "id": "apostille-mirror",
        "url": "https://arhiv1973b.github.io/apostille-mirror/",
        "critical": True,
        "group": "actor",
        "note": "Forensic hub mirror",
    },
    {
        "id": "sample-pdf",
        "url": "https://arhiv1973b.github.io/apostille-archive-english/apostille_IMWM44AZGX6N6_2013073817848.pdf",
        "critical": True,
        "group": "actor",
        "note": "Sample PDF download (HEAD)",
        "method": "HEAD",
        "expect_pdf": True,
    },
]


def check_one(ep: dict, timeout: float = 15.0) -> dict:
    url = ep["url"]
    method = ep.get("method", "GET")
    t0 = time.perf_counter()
    out = {
        "id": ep["id"],
        "url": url,
        "group": ep.get("group"),
        "critical": bool(ep.get("critical")),
        "note": ep.get("note"),
        "ok": False,
        "status": None,
        "ms": None,
        "error": None,
        "content_type": None,
        "ssl_ok": None,
    }

    curl_bin = shutil.which("curl")
    if curl_bin:
        cmd = [
            curl_bin, "-sS", "-L", "-o", "/dev/null",
            "-w", "%{http_code}|%{content_type}|%{ssl_verify_result}|%{errormsg}",
            "--connect-timeout", str(min(8, int(timeout))),
            "--max-time", str(int(timeout)),
            "-A", UA,
            "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
            "-H", "Accept-Language: en-US,en;q=0.9,ro;q=0.8,ru;q=0.7",
        ]
        if method.upper() == "HEAD":
            cmd.append("-I")
        cmd.append(url)
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
            line = (p.stdout or "").strip().splitlines()[-1] if p.stdout else ""
            parts = line.split("|")
            while len(parts) < 4:
                parts.append("")
            code_s, ctype, ssl_vr, errmsg = parts[0], parts[1], parts[2], parts[3]
            if code_s.isdigit():
                out["status"] = int(code_s)
            out["content_type"] = ctype or None
            if ssl_vr.isdigit():
                out["ssl_ok"] = ssl_vr == "0"
            if out["status"] == 0 or out["status"] is None:
                out["error"] = errmsg or (p.stderr or "").strip() or "connection failed"
                out["ok"] = False
                if out["ssl_ok"] is False or "SSL" in (out["error"] or "").upper():
                    out["ssl_ok"] = False
            else:
                if ep.get("expect_pdf"):
                    ct = (out["content_type"] or "").lower()
                    out["ok"] = out["status"] in (200, 206) and (
                        "pdf" in ct or "octet-stream" in ct
                    )
                else:
                    out["ok"] = 200 <= out["status"] < 400
                if not out["ok"] and not out["error"]:
                    out["error"] = f"HTTP {out['status']}"
        except Exception as e:
            out["error"] = f"curl: {type(e).__name__}: {e}"
            out["ok"] = False
    else:
        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(
                url, method=method,
                headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8"},
            )
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                out["status"] = resp.status
                out["content_type"] = resp.headers.get("Content-Type")
                out["ssl_ok"] = True
                if ep.get("expect_pdf"):
                    ct = (out["content_type"] or "").lower()
                    out["ok"] = resp.status in (200, 206) and (
                        "pdf" in ct or "octet-stream" in ct
                    )
                else:
                    out["ok"] = 200 <= resp.status < 400
        except urllib.error.HTTPError as e:
            out["status"] = e.code
            out["error"] = str(e.reason)
            out["ssl_ok"] = True
            out["ok"] = False
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"
            out["ok"] = False
            if "SSL" in type(e).__name__ or "certificate" in str(e).lower():
                out["ssl_ok"] = False

    out["ms"] = round((time.perf_counter() - t0) * 1000)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Monitor apostille API / endpoint availability")
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--json-out", default="api_availability_report.json")
    args = ap.parse_args()

    print(f"[1/2] Checking {len(ENDPOINTS)} endpoints\u2026")
    results: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(check_one, ep, args.timeout) for ep in ENDPOINTS]
        for fut in concurrent.futures.as_completed(futs):
            r = fut.result()
            results.append(r)
            mark = "OK  " if r["ok"] else "FAIL"
            crit = "CRIT" if r["critical"] else "info"
            print(
                f"  [{crit}] {mark}  {r['id']:28}  "
                f"status={r['status']}  {r['ms']}ms  {r['error'] or r['content_type'] or ''}"
            )

    order = {ep["id"]: i for i, ep in enumerate(ENDPOINTS)}
    results.sort(key=lambda r: order.get(r["id"], 999))

    critical_fail = [r for r in results if r["critical"] and not r["ok"]]
    soft_fail = [r for r in results if not r["critical"] and not r["ok"]]
    ok_n = sum(1 for r in results if r["ok"])

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "ok": ok_n,
        "failed": len(results) - ok_n,
        "critical_failed": len(critical_fail),
        "soft_failed": len(soft_fail),
        "critical_failures": critical_fail,
        "soft_failures": soft_fail,
        "results": results,
    }

    Path(args.json_out).write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = [
        "# API / Endpoint Availability Report",
        "",
        f"- **When:** {report['generated_at']}",
        f"- **Total:** {report['total']}",
        f"- **OK:** {report['ok']}",
        f"- **FAIL:** {report['failed']} (critical: {report['critical_failed']}, soft: {report['soft_failed']})",
        "",
        "## Results",
        "",
        "| ID | Group | Critical | Status | ms | OK | Error |",
        "|----|-------|----------|--------|----|----|-------|",
    ]
    for r in results:
        md.append(
            f"| `{r['id']}` | {r['group']} | {r['critical']} | {r['status']} | "
            f"{r['ms']} | {r['ok']} | {r['error'] or ''} |"
        )
    if critical_fail:
        md += ["", "## Critical failures", ""]
        for r in critical_fail:
            md.append(f"- **{r['id']}** `{r['url']}` \u2014 {r['error'] or r['status']}")
    Path(Path(args.json_out).with_suffix(".md")).write_text(
        "\n".join(md) + "\n", encoding="utf-8"
    )

    print()
    print("[2/2] Summary")
    print(f"  Total           : {report['total']}")
    print(f"  OK              : {report['ok']}")
    print(f"  Critical FAIL   : {report['critical_failed']}")
    print(f"  Soft FAIL       : {report['soft_failed']}")
    print(f"  JSON            : {args.json_out}")

    return 1 if critical_fail else 0


if __name__ == "__main__":
    sys.exit(main())
