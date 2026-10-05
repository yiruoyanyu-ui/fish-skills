"""Storage adapters; write credentials belong to the publisher, not the Agent."""
from __future__ import annotations

import io
import json
import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

from .bundle import MAX_FILE_BYTES, safe_path, version_name

MAX_READ = 20 * 1024 * 1024


class FileStore:
    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def _path(self, key):
        safe_path(key)
        path = self.root.joinpath(key).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("Outside store")
        return path

    def read(self, key):
        p = self._path(key)
        if not p.exists():
            raise FileNotFoundError(key)
        if p.stat().st_size > MAX_READ:
            raise ValueError("Stored object too large")
        return p.read_bytes()

    def write(self, key, data, immutable=False):
        p = self._path(key)
        p.parent.mkdir(parents=True, exist_ok=True)
        if immutable:
            try:
                with p.open("xb") as f:
                    f.write(data)
            except FileExistsError:
                if p.read_bytes() != data:
                    raise ValueError(f"Refusing to overwrite release object: {key}")
        else:
            temporary = p.with_name(p.name + f".{os.getpid()}.tmp")
            temporary.write_bytes(data)
            temporary.replace(p)


class R2Store:
    def __init__(self):
        import boto3
        from botocore.config import Config
        required = ["R2_ACCOUNT_ID", "R2_BUCKET", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY"]
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise ValueError("Missing R2 configuration names: " + ", ".join(missing))
        self.bucket = os.environ["R2_BUCKET"]
        self.prefix = safe_path(os.getenv("FISH_SKILLS_PREFIX", "fish-skills"))
        self.client = boto3.client("s3", endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
                                   region_name="auto", aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
                                   aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
                                   config=Config(connect_timeout=10, read_timeout=30, retries={"max_attempts": 3}))

    def read(self, key):
        from botocore.exceptions import ClientError
        safe_path(key)
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=f"{self.prefix}/{key}")
        except ClientError as e:
            if e.response["Error"]["Code"] in {"NoSuchKey", "404"}:
                raise FileNotFoundError(key) from None
            raise
        body = response["Body"]
        try:
            if response["ContentLength"] > MAX_READ:
                raise ValueError("Stored object too large")
            data = body.read(MAX_READ + 1)
            if len(data) > MAX_READ:
                raise ValueError("Stored object too large")
            return data
        finally:
            body.close()

    def write(self, key, data, immutable=False):
        from botocore.exceptions import ClientError
        safe_path(key)
        args = {"Bucket": self.bucket, "Key": f"{self.prefix}/{key}", "Body": data,
                "ContentType": "application/json" if key.endswith(".json") else "text/plain; charset=utf-8",
                "CacheControl": "public, max-age=31536000, immutable" if immutable else "no-cache"}
        if immutable:
            args["IfNoneMatch"] = "*"
        try:
            self.client.put_object(**args)
        except ClientError as e:
            if immutable and e.response["Error"]["Code"] in {"PreconditionFailed", "412"}:
                if self.read(key) != data:
                    raise ValueError(f"Refusing to overwrite release object: {key}") from None
            else:
                raise


class NoCredentialRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        result = super().redirect_request(req, fp, code, msg, headers, newurl)
        if result and urllib.parse.urlparse(newurl).netloc != urllib.parse.urlparse(req.full_url).netloc:
            result.remove_header("Authorization")
        return result


class GitHubStore:
    """Read-only fallback for published GitHub Release ZIPs, including private repos."""
    def __init__(self):
        self.repo = os.environ["FISH_SKILLS_GITHUB_REPOSITORY"]
        if len(self.repo.split("/")) != 2 or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_./" for c in self.repo):
            raise ValueError("Invalid GitHub owner/repo")
        self.token = os.getenv("FISH_SKILLS_GITHUB_TOKEN", "")
        if not self.token:
            try:
                auth = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
                if auth.returncode == 0:
                    self.token = auth.stdout.strip()
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
        self.bundles = {}
        self.channels = {}

    def _get(self, url, binary=False):
        headers = {"Accept": "application/octet-stream" if binary else "application/vnd.github+json",
                   "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "fish-skills"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, headers=headers)
        opener = urllib.request.build_opener(NoCredentialRedirect())
        with opener.open(request, timeout=30) as response:
            data = response.read(MAX_READ + 1)
        if len(data) > MAX_READ:
            raise ValueError("GitHub response too large")
        return data if binary else json.loads(data)

    def _bundle(self, release):
        version = version_name(release["tag_name"].removeprefix("v"))
        if version not in self.bundles:
            asset = next((a for a in release["assets"] if a["name"] == f"fish-skills-{version}.zip"), None)
            if not asset:
                raise FileNotFoundError("Published bundle asset is missing")
            data = self._get(asset["url"], binary=True)
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                if len(z.namelist()) != len(set(z.namelist())) or sum(i.file_size for i in z.infolist()) > MAX_READ:
                    raise ValueError("Invalid release ZIP")
                payload = {safe_path(i.filename): z.read(i) for i in z.infolist()}
            manifest = json.loads(payload["manifest.json"])
            if manifest["version"] != version:
                raise ValueError("Release tag and content version mismatch")
            from .bundle import verify
            verify(manifest, payload.__getitem__)
            self.bundles[version] = payload
        return version, self.bundles[version]

    def read(self, key):
        safe_path(key)
        if key.startswith("channels/"):
            channel = key.split("/")[-1].removesuffix(".json")
            if channel not in {"preview", "stable"}:
                raise ValueError("Invalid channel")
            cached = self.channels.get(channel)
            if cached and time.monotonic() - cached[0] < 60:
                return cached[1]
            releases = self._get(f"https://api.github.com/repos/{self.repo}/releases?per_page=100")
            for release in releases:
                if release["draft"] or bool(release["prerelease"]) != (channel == "preview"):
                    continue
                version, payload = self._bundle(release)
                manifest = json.loads(payload["manifest.json"])
                if manifest["channel"] != channel:
                    continue
                from .bundle import canonical, sha256
                pointer = canonical({"version": version, "manifest_sha256": sha256(payload["manifest.json"]), "channel": channel})
                self.channels[channel] = (time.monotonic(), pointer)
                return pointer
            raise FileNotFoundError(f"No published release for {channel}")
        prefix, version, path = key.split("/", 2)
        if prefix != "releases":
            raise ValueError("Unsupported object key")
        version_name(version)
        if version not in self.bundles:
            release = self._get(f"https://api.github.com/repos/{self.repo}/releases/tags/v{version}")
            if release["draft"]:
                raise FileNotFoundError("Draft release is unavailable")
            self._bundle(release)
        try:
            return self.bundles[version][path]
        except KeyError:
            raise FileNotFoundError(path) from None


def configured_store():
    backend = os.getenv("FISH_SKILLS_BACKEND", "file")
    if backend == "file":
        return FileStore(os.getenv("FISH_SKILLS_STORE", ".store"))
    if backend == "r2":
        return R2Store()
    if backend == "github":
        return GitHubStore()
    raise ValueError("FISH_SKILLS_BACKEND must be file, r2 or github")
