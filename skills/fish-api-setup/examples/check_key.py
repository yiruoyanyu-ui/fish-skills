"""Check the Fish API key and API wallet without printing the key. Read FISH_API_KEY or a local .env. Exit codes: 0 funded, 1 missing key, 2 invalid, 3 error, 4 valid but unfunded."""
import os
import re
import sys

import requests


def load_key():
    key = os.environ.get("FISH_API_KEY")
    if key:
        return key.strip()
    try:
        for line in open(".env", encoding="utf-8"):
            m = re.match(r"\s*FISH_API_KEY\s*=\s*(.+?)\s*$", line)
            if m:
                return m.group(1).strip().strip("\"'")
    except FileNotFoundError:
        pass
    return None


def main():
    key = load_key()
    if not key:
        print("FISH_API_KEY not found in environment or local .env")
        return 1
    r = requests.get(
        "https://api.fish.audio/wallet/self/api-credit",
        headers={"Authorization": f"Bearer {key}"},
        timeout=30,
    )
    if r.status_code == 401:
        print("Invalid key (401)")
        return 2
    if r.status_code != 200:
        print(f"Unexpected HTTP {r.status_code} {r.text[:200]}")
        return 3
    credit = float(r.json()["credit"])
    print(f"Valid key; API wallet balance {credit:.6f}(separate from platform credits)")
    if credit <= 0:
        print("Zero API balance: generation returns 402; configure API funds in the developer area")
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
