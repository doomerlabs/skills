#!/usr/bin/env python3
"""Bootstrap a verified Doomer CLI, then delegate installation to that CLI."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import ssl
import subprocess
import tarfile
import tempfile
import urllib.request

STABLE_CHANNEL = 'https://downloads.doomer.ai/cli/stable.json'
MAX_ARCHIVE = 32 * 1024 * 1024
MAX_BINARY = 64 * 1024 * 1024


def download(url, limit):
    if not url.startswith('https://'):
        raise ValueError('HTTPS is required')
    request = urllib.request.Request(url, headers={'User-Agent': 'doomer-bootstrap/2'})
    context = ssl.create_default_context()
    # macOS Python installations can have an empty interpreter CA bundle even
    # though the OS trust bundle is present. Keep verification enabled and load
    # that bundle unless the user explicitly selected a different trust store.
    if (platform.system() == 'Darwin'
            and not os.environ.get('SSL_CERT_FILE')
            and not os.environ.get('SSL_CERT_DIR')
            and Path('/etc/ssl/cert.pem').is_file()):
        context.load_verify_locations(cafile='/etc/ssl/cert.pem')
    with urllib.request.urlopen(request, timeout=60, context=context) as response:
        if not response.url.startswith('https://'):
            raise ValueError('Insecure download redirect')
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError('Download exceeded its size limit')
    return data


def extract_binary(archive):
    allowed_files = {'LICENSE', 'README.md', 'docs/release.md', 'docs/trust-model.md', 'doomer'}
    allowed_directories = {'', '.', 'docs'}
    seen = set()
    binary = None
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as source:
        for member in source:
            name = member.name.removeprefix('./').rstrip('/')
            if name in seen:
                raise ValueError('Duplicate release archive member')
            seen.add(name)
            if member.isdir() and name in allowed_directories:
                continue
            if name not in allowed_files or not member.isfile():
                raise ValueError('Unexpected release archive member or file type')
            limit = MAX_BINARY if name == 'doomer' else 1024 * 1024
            if member.size > limit or member.size < 0:
                raise ValueError('Release archive member exceeds its size limit')
            if name == 'doomer':
                if member.size == 0 or not member.mode & 0o111:
                    raise ValueError('Release executable is empty or not executable')
                binary = source.extractfile(member).read()
    if binary is None:
        raise ValueError('Release executable is missing')
    return binary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--personal', action='store_true')
    parser.add_argument('--repo', default='.')
    parser.add_argument('--adopt', action='store_true', help='Explicitly replace an unmanaged launcher with a backup')
    args = parser.parse_args()
    system = {'Darwin': 'darwin', 'Linux': 'linux'}.get(platform.system())
    arch = {'arm64': 'arm64', 'aarch64': 'arm64', 'x86_64': 'amd64', 'AMD64': 'amd64'}.get(platform.machine())
    if not system or not arch:
        raise ValueError('Doomer supports macOS/Linux on arm64/amd64')
    channel = json.loads(download(STABLE_CHANNEL, 1024 * 1024))
    version = channel.get('version', '')
    if channel.get('schema_version') != 1 or not re.fullmatch(r'20\d{2}\.\d{1,2}\.\d{1,2}\.[1-9]\d*', version):
        raise ValueError('Invalid stable Doomer channel')
    name = f'doomer_{version}_{system}_{arch}.tar.gz'
    asset = channel.get('assets', {}).get(f'{system}_{arch}', {})
    archive_url = f'https://downloads.doomer.ai/cli/releases/{version}/{name}'
    if asset.get('url') != archive_url:
        raise ValueError('Stable channel archive does not match its release')
    expected = asset.get('sha256', '')
    if not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise ValueError('Release archive checksum is missing')
    archive = download(archive_url + '?download=1', MAX_ARCHIVE)
    if hashlib.sha256(archive).hexdigest() != expected:
        raise ValueError('Release archive checksum mismatch')
    with tempfile.TemporaryDirectory(prefix='doomer-bootstrap-') as directory:
        binary = Path(directory) / 'doomer'
        binary.write_bytes(extract_binary(archive))
        binary.chmod(0o700)
        info = json.loads(subprocess.check_output([str(binary), 'runtime-info'], timeout=10))
        if info.get('managed_protocol') != 2:
            raise ValueError('Published CLI does not support the managed bootstrap yet')
        command = [str(binary), 'install', '--runtime']
        command += ['--personal'] if args.personal else ['--repo', os.path.abspath(args.repo)]
        if args.adopt:
            command.append('--adopt')
        subprocess.run(command, check=True)


if __name__ == '__main__':
    main()
