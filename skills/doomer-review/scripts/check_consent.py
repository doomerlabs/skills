"""Read existing CLI upload approval without running Doomer or changing state."""
import argparse
import base64
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

API = "https://doomer.ai/api"
PROFILE = "default"


def read_json(path):
    if not path.exists():
        return {}
    if path.stat().st_size > 4 * 1024 * 1024:
        raise ValueError("state too large")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError("expected object")
    return value


def config_root():
    if os.environ.get("DOOMER_CONFIG_DIR"):
        return Path(os.environ["DOOMER_CONFIG_DIR"]).resolve()
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "doomer"
    return Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / "doomer"


def check(repo, common, base):
    state = base / "watch" / hashlib.sha256((API + "\0" + PROFILE).encode()).hexdigest()
    source = state / "config.json"
    result = dict(approved=False, reason="no_saved_approval", source=str(source),
                  repository=str(repo), api=API, profile=PROFILE)
    try:
        cfg = read_json(source)
        if not cfg:
            return result
        if (cfg.get("version") != 1 or cfg.get("explicit_consent") is not True
                or cfg.get("api_url") != API or cfg.get("profile") != PROFILE
                or not cfg.get("consented_at")):
            return dict(result, reason="approval_scope_mismatch")
        if (str(repo) not in cfg.get("directories", [])
                and str(common) not in cfg.get("repository_ids", [])):
            return dict(result, reason="repository_not_approved")
        key = f"auth:v2:{len(API)}:{API}:{PROFILE}"
        auth = read_json(base / "config.json").get("auths", {}).get(key, {})
        token = auth.get("token", "")
        if token and auth.get("expires_at"):
            expiry = datetime.fromisoformat(auth["expires_at"].replace("Z", "+00:00"))
            if expiry.tzinfo is None:
                raise ValueError("invalid expiry")
            if expiry <= datetime.now(timezone.utc) + timedelta(seconds=30):
                token = ""
        if not token:
            anon = read_json(state / "anonymous.json")
            token = anon.get("Token", "")
            if (anon.get("API") != API or anon.get("Profile") != PROFILE
                    or not re.fullmatch(r"doomer_anon_[A-Za-z0-9_-]{43}", token)):
                return dict(result, reason="identity_unavailable")
            if len(base64.urlsafe_b64decode(token[len("doomer_anon_"):] + "=")) != 32:
                return dict(result, reason="identity_unavailable")
        if hashlib.sha256(token.encode()).hexdigest() != cfg.get("account_key"):
            return dict(result, reason="identity_changed")
        return dict(result, approved=True, reason="existing_browser_approval")
    except (OSError, ValueError, TypeError, AttributeError):
        return dict(result, reason="unreadable_saved_state")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    try:
        def git(*flags):
            return subprocess.check_output(["git", "-C", args.repo, "rev-parse", *flags],
                                           text=True, stderr=subprocess.DEVNULL).strip()
        repo = Path(git("--show-toplevel")).resolve()
        common = Path(git("--path-format=absolute", "--git-common-dir")).resolve()
        result = check(repo, common, config_root())
    except (OSError, subprocess.CalledProcessError):
        result = dict(approved=False, reason="repository_unavailable")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
