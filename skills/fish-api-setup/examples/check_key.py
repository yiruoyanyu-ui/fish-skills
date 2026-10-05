"""验证 Fish Audio API key 并读取 API 钱包余额（免费，不消耗额度）。
key 来源：环境变量 FISH_API_KEY，其次当前目录 .env。绝不打印 key。
退出码：0=有效且有余额  1=未找到 key  2=key 无效  3=其他错误  4=有效但余额为 0"""
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
        print("未找到 FISH_API_KEY（环境变量或 .env）")
        return 1
    r = requests.get(
        "https://api.fish.audio/wallet/self/api-credit",
        headers={"Authorization": f"Bearer {key}"},
        timeout=30,
    )
    if r.status_code == 401:
        print("key 无效（401 Invalid Token）")
        return 2
    if r.status_code != 200:
        print(f"异常：HTTP {r.status_code} {r.text[:200]}")
        return 3
    credit = float(r.json()["credit"])
    print(f"key 有效；API 钱包余额 {credit:.6f}（与平台 credits 独立）")
    if credit <= 0:
        print("余额为 0：生成类接口会返回 402，请到 fish.audio/app/developers 充值")
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
