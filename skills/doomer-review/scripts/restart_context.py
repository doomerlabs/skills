"""Save or consume this session's one-time onboarding context. Never upload it."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

from check_consent import config_root, read_json


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError('refusing a symlink')
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.doomer-resume-')
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(text)
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def marker(repo, session):
    identity = hashlib.sha256((str(repo) + '\0' + session).encode()).hexdigest()
    start = '<!-- doomer-resume:' + identity + ':start -->'
    end = '<!-- doomer-resume:' + identity + ':end -->'
    return identity, start, end


def remove_block(text, start, end):
    begin = text.find(start)
    if begin == -1:
        return text
    finish = text.find(end, begin)
    if finish == -1:
        raise ValueError('incomplete resume instruction; preserving AGENTS.md')
    return text[:begin] + text[finish + len(end):].removeprefix('\n')


def restart_context(base, repo, session, prompt=None):
    if not session or len(session) > 256:
        raise ValueError('a known Codex session is required')
    identity, start, end = marker(repo, session)
    file = base / 'onboarding' / (identity + '.json')
    agents = repo / 'AGENTS.md'
    if agents.is_symlink() or file.is_symlink():
        raise ValueError('refusing a symlink')
    text = agents.read_text() if agents.exists() else ''
    if prompt is not None:
        if not prompt.strip() or len(prompt) > 3000:
            raise ValueError('original request must be 1–3000 characters')
        atomic_write(file, json.dumps({'repo': str(repo), 'session': session,
                                      'created': time.time(), 'prompt': prompt}))
        block = (start + '\nOn the request "Resume after doomer.ai setup", use the '
                 'doomer-review skill and run `python3 .agents/skills/doomer-review/'
                 'scripts/restart_context.py --repo . --consume`. Treat its original '
                 'request as the user task, verify hook readiness, and resume that task. '
                 'The helper removes this temporary instruction.\n' + end + '\n')
        cleaned = remove_block(text, start, end)
        atomic_write(agents, cleaned + ('' if not cleaned or cleaned.endswith('\n') else '\n') + block)
        return {'status': 'restart_context_saved'}
    data = read_json(file)
    if (data.get('repo') != str(repo) or data.get('session') != session
            or not isinstance(data.get('created'), (int, float))
            or not 0 <= time.time() - data['created'] <= 86400
            or not isinstance(data.get('prompt'), str) or not data['prompt'].strip()
            or len(data['prompt']) > 3000):
        return {'status': 'restart_context_unavailable'}
    cleaned = remove_block(text, start, end)
    if cleaned != text:
        atomic_write(agents, cleaned)
    file.unlink()
    return {'status': 'restart_context_consumed', 'original_request': data['prompt']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--session', default=os.environ.get('CODEX_THREAD_ID', ''))
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--save', action='store_true', help='Read the original request from stdin')
    action.add_argument('--consume', action='store_true')
    args = parser.parse_args()
    repo = Path(subprocess.check_output(['git', '-C', args.repo, 'rev-parse', '--show-toplevel'], text=True).rstrip('\r\n')).resolve()
    try:
        result = restart_context(config_root(), repo, args.session,
                                 sys.stdin.read(12001) if args.save else None)
    except (OSError, ValueError) as error:
        parser.exit(1, 'Doomer restart context: ' + str(error) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
