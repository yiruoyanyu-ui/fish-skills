"""GitHub Release publisher; resumable drafts, immutable published artifacts."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

from fish_skills.bundle import sha256
from fish_skills.publish import publish
from fish_skills.storage import R2Store


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


def main():
    manifest = json.loads(Path("dist/manifest.json").read_text())
    version = manifest["version"]
    tag = "v" + version
    archive = Path(f"dist/fish-skills-{version}.zip")
    repo = os.environ["GITHUB_REPOSITORY"]
    commit = os.environ["GITHUB_SHA"]
    if manifest["source_commit"] != commit:
        raise ValueError("Build commit mismatch")
    backend = os.environ.get("PUBLISH_BACKEND", "github")
    if backend not in {"github", "r2"}:
        raise ValueError("Unsupported publication backend")
    store = R2Store() if backend == "r2" else None  # Check configuration before creating a draft.
    tag_lookup = subprocess.run(["gh", "api", f"repos/{repo}/git/ref/tags/{tag}"], capture_output=True, text=True)
    if tag_lookup.returncode:
        if "404" not in tag_lookup.stderr:
            raise RuntimeError("Cannot inspect release tag")
        # Draft releases do not reliably create refs; create and freeze the tag first.
        gh("api", "--method", "POST", f"repos/{repo}/git/refs", "-f", f"ref=refs/tags/{tag}", "-f", f"sha={commit}")
    ref = json.loads(gh("api", f"repos/{repo}/git/ref/tags/{tag}"))["object"]
    while ref["type"] == "tag":
        ref = json.loads(gh("api", f"repos/{repo}/git/tags/{ref['sha']}"))["object"]
    if ref["type"] != "commit" or ref["sha"] != commit:
        raise ValueError("Release tag already belongs to a different commit")
    # The by-tag endpoint may return 404 for draft releases; list with write access instead.
    pages = json.loads(gh("api", "--paginate", "--slurp", f"repos/{repo}/releases?per_page=100"))
    release = next((r for page in pages for r in page if r["tag_name"] == tag), None)
    if release is None:
        body = {"tag_name": tag, "target_commitish": commit, "draft": True,
                "prerelease": manifest["channel"] == "preview", "name": f"Fish Skills {version}",
                "body": Path("docs/RELEASE_NOTES.md").read_text()}
        with tempfile.NamedTemporaryFile("w", suffix=".json") as file:
            json.dump(body, file)
            file.flush()
            release = json.loads(gh("api", "--method", "POST", f"repos/{repo}/releases", "--input", file.name))
    expected = [archive, Path("dist/manifest.json"), Path("dist/checksums.json")]
    assets = {a["name"]: a for a in release["assets"]}
    for path in expected:
        if path.name in assets:
            # gh download handles private assets without exposing tokens in commands/output.
            target = Path("dist/existing")
            target.mkdir(exist_ok=True)
            gh("release", "download", tag, "--repo", repo, "--pattern", path.name, "--dir", str(target), "--clobber")
            if sha256((target / path.name).read_bytes()) != sha256(path.read_bytes()):
                raise ValueError("Existing release asset differs; bump the content version")
        else:
            if not release["draft"]:
                raise ValueError("Published release is incomplete; refusing to mutate it")
            gh("release", "upload", tag, str(path), "--repo", repo)
    if store:
        result = publish(store, archive, activate=True)
        Path("dist/r2-publication.json").write_text(json.dumps(result, indent=2) + "\n")
    if release["draft"]:
        gh("api", "--method", "PATCH", f"repos/{repo}/releases/{release['id']}", "-F", "draft=false")
    print(json.dumps({"version": version, "channel": manifest["channel"], "backend": backend,
                      "release_url": release["html_url"]}))


if __name__ == "__main__":
    main()
