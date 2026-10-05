"""Shared reader used by MCP and by a future Fish platform integration."""
from __future__ import annotations

import json
import os
import time

from .bundle import MAX_FILE_BYTES, safe_path, sha256, version_name


class SkillReader:
    def __init__(self, store, channel="preview"):
        if channel not in {"preview", "stable"}:
            raise ValueError("Invalid channel")
        self.store = store
        self.channel = channel
        self.pointer = None
        self.manifests = {}
        self.files = {}

    def _manifest(self, version=None):
        expected_hash = None
        if version is None:
            if self.pointer is None or time.monotonic() - self.pointer[0] >= 60:
                pointer = json.loads(self.store.read(f"channels/{self.channel}.json"))
                if pointer["channel"] != self.channel:
                    raise ValueError("Channel mismatch")
                self.pointer = (time.monotonic(), pointer)
            pointer = self.pointer[1]
            version = pointer["version"]
            expected_hash = pointer["manifest_sha256"]
        version_name(version)
        if version not in self.manifests:
            raw = self.store.read(f"releases/{version}/manifest.json")
            manifest = json.loads(raw)
            if manifest["version"] != version or manifest["schema_version"] != 1:
                raise ValueError("Manifest version/schema mismatch")
            self.manifests[version] = (manifest, sha256(raw))
        manifest, digest = self.manifests[version]
        if expected_hash and digest != expected_hash:
            raise ValueError("Manifest integrity check failed")
        return manifest

    def list_skills(self, version=None):
        manifest = self._manifest(version)
        return {"version": manifest["version"], "channel": manifest["channel"],
                "source_commit": manifest["source_commit"], "skills": manifest["skills"]}

    def get_file(self, version: str, path: str):
        safe_path(path)
        manifest = self._manifest(version)
        item = next((f for f in manifest["files"] if f["path"] == path), None)
        if item is None:
            raise FileNotFoundError("Path is not in this version's manifest")
        key = (version, path)
        if key not in self.files:
            data = self.store.read(f"releases/{version}/{path}")
            if len(data) > MAX_FILE_BYTES or len(data) != item["bytes"] or sha256(data) != item["sha256"]:
                raise ValueError("File integrity check failed")
            self.files[key] = data.decode("utf-8")
        return {"version": version, "path": path, "mime_type": item["mime_type"],
                "bytes": item["bytes"], "sha256": item["sha256"], "content": self.files[key]}

    def get_instructions(self, skill_id: str, version=None):
        manifest = self._manifest(version)
        skill = next((s for s in manifest["skills"] if s["id"] == skill_id), None)
        if skill is None:
            raise FileNotFoundError("Unknown Skill ID in this version")
        file = self.get_file(manifest["version"], skill["entry"])
        return {"skill_id": skill_id, "version": file["version"], "channel": manifest["channel"],
                "status": skill["status"], "source_commit": manifest["source_commit"],
                "entry_path": skill["entry"], "content_sha256": file["sha256"],
                "instructions_markdown": file["content"],
                "available_paths": [f["path"] for f in manifest["files"]],
                "delivery_instructions": (
                    "Pin this version for the entire task. Resolve references relative to entry_path; "
                    "fetch the resulting package path with get_skill_file(version, path). "
                    "For fish-media:<name> routing, call get_skill_instructions(skill_id=<name>, version=this version). "
                    "Use the separately connected Fish Audio MCP for execution. "
                    "Fetching these documents neither generates media nor installs scripts. "
                    "Check current execution tools/models and remain within the user's spending authorization. "
                    "Dormant entries are archived documentation, not an executable supported workflow."
                )}
