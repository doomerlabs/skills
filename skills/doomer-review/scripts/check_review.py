"""Read this Codex session's local review state; never upload or change it."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import time
from urllib.parse import urlsplit

from check_consent import API, PROFILE, config_root, read_json


def key(value):
    return hashlib.sha256(value.encode()).hexdigest()


def check(root, repo, session, turn_id=None):
    if not session:
        return {"status": "session_unknown"}
    try:
        turn = read_json(root / "turns" / (key(session) + ".json"))
        owner = turn.get("Owner", {})
        if owner.get("session") != session or not owner.get("turn") or not turn.get("Prompt", "").strip():
            return {"status": "prompt_not_captured"}
        state = read_json(root / "repositories" / (key(str(repo)) + ".json"))
        if any(op.get("Owner") != owner for op in state.get("Active", {}).values()):
            return {"status": "ownership_ambiguous"}
        if turn_id is None:
            return {"status": "prompt_captured", "turn": owner["turn"]}
        if owner["turn"] != turn_id:
            return {"status": "turn_changed"}
        if state.get("Ambiguous") or any(op.get("Owner") != owner for op in state.get("Active", {}).values()):
            return {"status": "ownership_ambiguous"}
        if state.get("Owner") != owner or not state.get("Fingerprint"):
            return {"status": "edit_not_observed"}
        feed = read_json(root / "reviews" / (key(str(repo)) + ".json"))
        if feed.get("Owner") != owner or feed.get("Fingerprint") != state["Fingerprint"]:
            return {"status": "assessment_pending" if state.get("HypothesesSubmitted") else "hypotheses_pending"}
        status = feed.get("AssessmentStatus")
        if status not in ("ready", "unavailable"):
            return {"status": "assessment_pending"}
        # Do not expose share tokens, prompts, source, or findings. The trusted
        # hook remains responsible for delivering and handling review feedback.
        pending = sum(p.get("ReviewID") == feed.get("ReviewID") for p in turn.get("Pending", []))
        result_status = "assessment_" + status
        if status == "ready" and feed.get("Leads") and (pending or feed.get("ReviewID") not in turn.get("Delivered", [])):
            result_status = "feedback_pending"
        return {"status": result_status, "review_id": feed.get("ReviewID"),
                "lead_count": len(feed.get("Leads", [])), "pending_responses": pending}
    except (OSError, ValueError, TypeError, AttributeError):
        return {"status": "state_unreadable"}



def review_link(root, repo, session):
    """Explicitly retrieve the latest link for this session, not a status check."""
    if not session:
        return {"status": "session_unknown"}
    try:
        feed = read_json(root / "reviews" / (key(str(repo)) + ".json"))
        if feed.get("Owner", {}).get("session") != session:
            return {"status": "review_link_unavailable"}
        link = feed.get("URL", "")
        url, origin = urlsplit(link), urlsplit(API)
        if (url.scheme != origin.scheme or url.netloc != origin.netloc
                or url.username or url.password or url.query
                or not re.fullmatch(r"/look-closer/[a-z0-9][a-z0-9_.~-]*/[a-z0-9][a-z0-9_.~-]*/[a-f0-9]{64}", url.path)):
            return {"status": "review_link_unavailable"}
        if feed.get("Anonymous") and not url.fragment:
            return {"status": "review_link_unavailable"}
        return {"status": "review_link_ready", "review_id": feed.get("ReviewID"),
                "url": link, "requires_sign_in": not bool(feed.get("Anonymous"))}
    except (OSError, ValueError, TypeError, AttributeError):
        return {"status": "state_unreadable"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--session", default=os.environ.get("CODEX_THREAD_ID", ""))
    parser.add_argument("--turn")
    parser.add_argument("--review-link", action="store_true", help="Return the complete latest review URL for this session, including private access tokens")
    parser.add_argument("--wait", type=int, default=0, choices=range(61), metavar="0..60")
    args = parser.parse_args()
    repo = Path(subprocess.check_output(["git", "-C", args.repo, "rev-parse", "--show-toplevel"], text=True).rstrip("\r\n")).resolve()
    root = config_root() / "watch" / key(API + "\0" + PROFILE)
    if args.review_link:
        print(json.dumps(review_link(root, repo, args.session)))
        return
    deadline = time.monotonic() + args.wait
    while True:
        result = check(root, repo, args.session, args.turn)
        if result["status"] != "assessment_pending" or time.monotonic() >= deadline:
            print(json.dumps(result))
            return
        time.sleep(min(1, max(0, deadline - time.monotonic())))


if __name__ == "__main__":
    main()
