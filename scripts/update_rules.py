#!/usr/bin/env python3
"""Extract policy-free DIRECT rule entries from Johnshall Top500."""
from __future__ import annotations
import argparse
import urllib.request
from pathlib import Path

UPSTREAM = "https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_top500_whitelist.conf"
TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6", "GEOIP", "USER-AGENT"}

def extract_direct(config: str) -> list[str]:
    in_rule = False
    results: set[str] = set()
    for raw in config.splitlines():
        line = raw.strip()
        if line.startswith("[") and line.endswith("]"):
            in_rule = line.casefold() == "[rule]"
            continue
        if not in_rule or not line or line.startswith(("#", ";")):
            continue
        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 3 or parts[0].upper() not in TYPES:
            continue
        if parts[2].casefold() != "direct":
            continue
        results.add(f"{parts[0].upper()},{parts[1]}")
    if len(results) < 100:
        raise ValueError(f"Suspiciously small DIRECT ruleset ({len(results)}); refusing to overwrite existing output")
    return sorted(results)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=UPSTREAM)
    parser.add_argument("--output", default="rules/top500-direct.list")
    args = parser.parse_args()
    req = urllib.request.Request(args.source, headers={"User-Agent": "shadowrocket-rule-sync/1.1"})
    with urllib.request.urlopen(req, timeout=35) as response:
        config = response.read().decode("utf-8-sig")
    rules = extract_direct(config)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("# Shadowrocket RULE-SET entries (policy assigned by caller).\n" + "\n".join(rules) + "\n", encoding="utf-8")
    print(f"Wrote {len(rules)} DIRECT rules to {output}")

if __name__ == "__main__":
    main()
