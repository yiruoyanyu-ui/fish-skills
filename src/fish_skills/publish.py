"""Publish all immutable objects, verify them, then switch one channel pointer."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .bundle import canonical, load_archive, sha256, verify, version_name


def promote(store, version: str, channel: str) -> dict:
    version_name(version)
    if channel not in {"preview", "stable"}:
        raise ValueError("Invalid channel")
    raw = store.read(f"releases/{version}/manifest.json")
    manifest = json.loads(raw)
    if manifest["version"] != version or manifest["channel"] != channel:
        raise ValueError("Cannot promote a bundle to a different channel")
    verify(manifest, lambda path: store.read(f"releases/{version}/{path}"))
    if channel == "stable":
        review = manifest.get("review") or {}
        if (review.get("status") != "approved" or review.get("version") != version
                or review.get("content_digest") != manifest["content_digest"]
                or not review.get("reviewer") or not review.get("evidence")):
            raise ValueError("Stable release has no matching approved review")
    previous = None
    try:
        previous = json.loads(store.read(f"channels/{channel}.json"))["version"]
    except FileNotFoundError:
        pass
    pointer = {"schema_version": 1, "channel": channel, "version": version,
               "manifest_sha256": sha256(raw), "source_commit": manifest["source_commit"],
               "previous_version": previous, "updated_at": datetime.now(timezone.utc).isoformat()}
    store.write(f"channels/{channel}.json", canonical(pointer))
    actual = json.loads(store.read(f"channels/{channel}.json"))
    if actual != pointer:
        raise ValueError("Channel pointer readback mismatch; another writer may be publishing")
    return pointer


def publish(store, archive: Path, activate: bool = False) -> dict:
    manifest, payload = load_archive(archive)
    version = manifest["version"]
    for name, data in payload.items():
        store.write(f"releases/{version}/{name}", data, immutable=True)
    raw = canonical(manifest)
    # Manifest is written only after all payload objects, but it alone is not activation.
    store.write(f"releases/{version}/manifest.json", raw, immutable=True)
    if store.read(f"releases/{version}/manifest.json") != raw:
        raise ValueError("Manifest readback mismatch")
    verify(manifest, lambda path: store.read(f"releases/{version}/{path}"))
    pointer = promote(store, version, manifest["channel"]) if activate else None
    return {"version": version, "channel": manifest["channel"], "uploaded_files": len(payload),
            "verified": True, "activated": activate, "pointer": pointer}
