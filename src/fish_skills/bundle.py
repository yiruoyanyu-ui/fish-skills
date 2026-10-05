"""Deterministic release bundles; Markdown remains data, never Python code."""
from __future__ import annotations

import hashlib
import json
import mimetypes
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

MAX_FILE_BYTES = 512 * 1024
VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9]+(?:[.-][a-z0-9]+)*)?")
SKILL_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def version_name(version: str) -> str:
    if not VERSION.fullmatch(version):
        raise ValueError("Invalid content version; expected e.g. 0.1.0-preview.1")
    return version


def safe_path(path: str) -> str:
    p = PurePosixPath(path)
    if not path or p.is_absolute() or ".." in p.parts or "\\" in path or str(p) != path:
        raise ValueError("File path must be a normalized, relative package path")
    return path


def verify(manifest: dict, read) -> None:
    version_name(manifest["version"])
    if manifest["schema_version"] != 1 or manifest["channel"] not in {"preview", "stable"}:
        raise ValueError("Unsupported manifest")
    seen = set()
    for file in manifest["files"]:
        path = safe_path(file["path"])
        if path in seen or not path.startswith("skills/"):
            raise ValueError("Duplicate or invalid payload path")
        seen.add(path)
        data = read(path)
        if len(data) != file["bytes"] or len(data) > MAX_FILE_BYTES or sha256(data) != file["sha256"]:
            raise ValueError(f"Integrity check failed: {path}")
    if sha256(canonical(manifest["files"])) != manifest["content_digest"]:
        raise ValueError("Content digest mismatch")
    ids = set()
    for skill in manifest["skills"]:
        if not SKILL_ID.fullmatch(skill["id"]) or skill["id"] in ids:
            raise ValueError("Invalid or duplicate Skill ID")
        ids.add(skill["id"])
        if skill["entry"] != f"skills/{skill['id']}/SKILL.md" or skill["entry"] not in seen:
            raise ValueError("Missing Skill entry")


def build(root: Path, output: Path) -> dict:
    root = root.resolve()
    config = json.loads((root / "release.json").read_text())
    version = version_name(config["version"])
    if config["channel"] not in {"preview", "stable"}:
        raise ValueError("Invalid release channel")
    files = []
    payload = {}
    for path in sorted((root / "skills").rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not allowed: {path.relative_to(root)}")
        if not path.is_file():
            continue
        name = path.relative_to(root).as_posix()
        safe_path(name)
        if path.suffix not in {".md", ".json", ".py"} or path.name.startswith("."):
            raise ValueError(f"Unexpected payload: {name}")
        data = path.read_bytes()
        if len(data) > MAX_FILE_BYTES:
            raise ValueError(f"Payload too large: {name}")
        text = data.decode("utf-8")
        if path.suffix == ".json":
            json.loads(text)
        if re.search(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}|-----BEGIN .*PRIVATE KEY-----)", text):
            raise ValueError(f"Possible credential in payload: {name}")
        payload[name] = data
        files.append({"path": name, "bytes": len(data), "sha256": sha256(data),
                      "mime_type": "text/markdown" if path.suffix == ".md" else mimetypes.guess_type(name)[0] or "text/plain"})
    if not files:
        raise ValueError("No Skill files")
    # Local relative document links are validated, including shared references.
    for name, data in payload.items():
        if not name.endswith(".md"):
            continue
        text = data.decode()
        refs = re.findall(r"`((?:\.\./|references/|examples/)[^`\s]+\.(?:md|json|py))`", text)
        refs += re.findall(r"\]\(((?:\.\./|references/|examples/)[^\s)]+)\)", text)
        for ref in refs:
            ref = ref.split("#", 1)[0]
            target = (root / name).parent.joinpath(ref).resolve()
            if not target.is_relative_to(root / "skills") or not target.is_file():
                raise ValueError(f"Missing/outside reference in {name}: {ref}")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--porcelain", "--", "skills", "release.json", "reviews"], cwd=root, text=True)
    if dirty:
        raise ValueError("Commit Skill content, config and review before building")
    manifest = {"schema_version": 1, "version": version, "channel": config["channel"],
                "source_commit": commit, "content_digest": sha256(canonical(files)),
                "skills": config["skills"], "files": files, "review": None}
    verify(manifest, payload.__getitem__)
    if config["channel"] == "stable":
        review = json.loads((root / "reviews" / f"{version}.json").read_text())
        if (review.get("status") != "approved" or review.get("version") != version
                or review.get("content_digest") != manifest["content_digest"]
                or not review.get("reviewer") or not review.get("evidence")):
            raise ValueError("Stable release needs a content-bound, approved review with evidence")
        manifest["review"] = review
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"fish-skills-{version}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in [("manifest.json", canonical(manifest)), *sorted(payload.items())]:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    (output / "manifest.json").write_bytes(canonical(manifest))
    (output / "checksums.json").write_bytes(canonical({archive.name: sha256(archive.read_bytes()),
                                                       "manifest.json": sha256(canonical(manifest))}))
    return {"version": version, "channel": manifest["channel"], "skills": len(manifest["skills"]),
            "files": len(files), "archive": str(archive), "content_digest": manifest["content_digest"]}


def load_archive(path: Path) -> tuple[dict, dict[str, bytes]]:
    with zipfile.ZipFile(path) as z:
        if len(z.namelist()) != len(set(z.namelist())):
            raise ValueError("Duplicate ZIP entries")
        if sum(i.file_size for i in z.infolist()) > 20 * 1024 * 1024:
            raise ValueError("Bundle too large")
        payload = {safe_path(i.filename): z.read(i) for i in z.infolist()}
    manifest = json.loads(payload.pop("manifest.json"))
    if set(payload) != {f["path"] for f in manifest["files"]}:
        raise ValueError("ZIP payload does not match manifest")
    verify(manifest, payload.__getitem__)
    return manifest, payload
