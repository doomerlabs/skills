import hashlib
import importlib.util
import io
import json
import ssl
from pathlib import Path
import tarfile
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class BootstrapTests(unittest.TestCase):
    def test_stable_contract_has_no_cli_pin_or_updater_workflow(self):
        text = (ROOT / 'skills/doomer-review/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('doomer-protocol: "2"', text)
        self.assertIn('doomer-update-policy: stable', text)
        self.assertIn('doomer prepare', text)
        self.assertIn('doomer prepare --task HANDLE', text)
        self.assertIn('doomer task repair HANDLE', text)
        # Keep the generated bootstrap bounded while allowing the explicit
        # Quick/Deep completion guidance shared with the CLI.
        self.assertLess(len((ROOT / 'skills/doomer-review/SKILL.md').read_bytes()), 10 * 1024)
        self.assertNotIn('self-update', text)
        self.assertNotIn('doomer-version:', text)
        self.assertIn('doomer-cli-range:', text)
        self.assertNotIn('/main/INSTALL.md', text)
        self.assertRegex(text, r'skills/[a-f0-9]{40}/INSTALL.md')
        self.assertIn(hashlib.sha256((ROOT / 'INSTALL.md').read_bytes()).hexdigest(), text)
        self.assertFalse((ROOT / 'skills/doomer-review/references').exists())

    def test_quick_completion_and_explicit_deep_guidance(self):
        text = (ROOT / 'skills/doomer-review/SKILL.md').read_text(encoding='utf-8')
        metadata = text.split('---', 2)[1]
        self.assertRegex(metadata, r'(?m)^  doomer-bootstrap-version: 2026\.11\.8\.10$')
        self.assertRegex(metadata, r"(?m)^  doomer-cli-range: '>=2026\.11\.7\.5'$")
        final = text.split('## Final source review\n', 1)[1].split('For requested installation', 1)[0]
        final = ' '.join(final.split())
        for requirement in [
            'Use task state and Quick readiness, not aggregate review status or `full_review.status`.',
            'Quick review of the latest submitted changes gates completion.',
            'Read Quick findings and record every response. After edits, resubmit and repeat.',
            'Deep continues in the background; its pending or failed status does not block successful Quick review.',
            'Do not fetch Deep results to finish; wait for Deep only when explicitly requested.',
            'Verify response delivery and current source with `doomer task finish HANDLE` before ending the turn.',
            'Only when the user explicitly requests Deep, use `review.id` from task status with `doomer review get REVIEW_ID --workspace --format json`, using the task\'s API URL and profile.',
            'Do not use this command as a prerequisite for automatic Quick completion.',
        ]:
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, final)
        self.assertNotIn('wait for Deep when enabled', final)

    def test_blocked_review_preserves_local_work_and_permission_boundaries(self):
        text = (ROOT / 'skills/doomer-review/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('doomer preflight --agent AGENT --repo .', text)
        self.assertIn('account or authorize uploads', text)
        self.assertIn('For a confirmed sandbox restriction', text)
        self.assertIn('continue authorized local edits and tests by default', text)
        self.assertEqual(text.count('If review is blocked,'), 1)
        self.assertEqual(text.count('Show complete clickable'), 1)
        self.assertLess(text.index('If review is blocked,'), text.index('Show complete clickable'))
        continuation = text.split('If review is blocked,', 1)[1].split('Show complete clickable', 1)[0]
        self.assertIn('Explicit earlier user requirements to wait or\nrequire review before editing take precedence.', continuation)
        self.assertIn('Do not ask whether to continue.', continuation)
        self.assertIn('Stop the denied transmission; keep uploads blocked.', continuation)
        self.assertIn('Silence is not upload consent.', continuation)
        self.assertIn('Do not retry explicit reviewer refusals.', continuation)
        self.assertIn('--base STARTING_COMMIT', text)
        self.assertIn('configured` means saved, not active', text)
        self.assertNotIn('ask once whether to continue local edits', text)
        guide = (ROOT / 'INSTALL.md').read_text(encoding='utf-8')
        self.assertIn('continue authorized local edits and tests by default', guide)
        self.assertIn('Do not ask whether to continue.', guide)
        self.assertNotIn('ask once whether to continue local edits', guide)

    def test_installer_is_pinned_and_scope_requires_a_choice(self):
        guide = (ROOT / 'INSTALL.md').read_text(encoding='utf-8')
        self.assertRegex(guide, r'skills/[a-f0-9]{40}/scripts/install.py')
        self.assertIn(hashlib.sha256((ROOT / 'scripts/install.py').read_bytes()).hexdigest(), guide)
        self.assertIn('ask personal versus team and wait', guide)
        self.assertIn('returns another protocol', guide)

    def test_summarized_instructions_recover_from_original(self):
        guide = (ROOT / 'INSTALL.md').read_text(encoding='utf-8')
        self.assertIn('curl -fsSL https://doomer.ai/install.md', guide)
        self.assertIn('all 64 checksum characters', guide)
        self.assertIn('Never reconstruct', guide)
        self.assertIn('unauthenticated HTTPS', guide)
        self.assertIn('same URL', guide)
        self.assertIn('Honor host or user access denials', guide)
        self.assertIn('installer URL and digest must equal', guide)

    def test_macos_download_loads_system_ca_bundle(self):
        loaded_contexts = []

        def record_roots(context, **kwargs):
            loaded_contexts.append((context, kwargs))

        response = MagicMock()
        response.url = 'https://example.invalid/file'
        response.read.return_value = b'verified'
        response.__enter__.return_value = response
        with patch.object(installer.platform, 'system', return_value='Darwin'), \
                patch.object(installer.ssl.SSLContext, 'load_verify_locations', new=record_roots), \
                patch.object(installer.Path, 'is_file', return_value=True), \
                patch.dict(installer.os.environ, {}, clear=True), \
                patch.object(installer.urllib.request, 'urlopen', return_value=response) as open_url:
            self.assertEqual(installer.download(response.url, 100), b'verified')
            context = open_url.call_args.kwargs['context']
            self.assertEqual(loaded_contexts, [(context, {'cafile': '/etc/ssl/cert.pem'})])
            self.assertIsInstance(context, ssl.SSLContext)
            self.assertTrue(context.check_hostname)
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)

    def test_explicit_ca_bundle_is_preserved(self):
        response = MagicMock()
        response.url = 'https://example.invalid/file'
        response.read.return_value = b'verified'
        response.__enter__.return_value = response
        with patch.object(installer.platform, 'system', return_value='Darwin'), \
                patch.object(installer.ssl.SSLContext, 'load_verify_locations') as load_roots, \
                patch.dict(installer.os.environ, {'SSL_CERT_FILE': '/custom/roots.pem'}, clear=True), \
                patch.object(installer.urllib.request, 'urlopen', return_value=response) as open_url:
            installer.download(response.url, 100)
            load_roots.assert_not_called()
            context = open_url.call_args.kwargs['context']
            self.assertIsInstance(context, ssl.SSLContext)
            self.assertTrue(context.check_hostname)
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)

    def test_stable_channel_avoids_api_discovery_and_verifies_archive(self):
        archive = b'fixture archive'
        version = '2026.11.7.5'
        name = f'doomer_{version}_linux_amd64.tar.gz'
        for failure in [None, 'checksum', 'version']:
            with self.subTest(failure=failure):
                asset_url = f'https://downloads.doomer.ai/cli/releases/{version}/{name}'
                channel = {'schema_version': 1, 'version': version, 'assets': {'linux_amd64': {
                    'url': asset_url if failure != 'version' else asset_url.replace(version, '2026.11.7.4'),
                    'sha256': hashlib.sha256(archive if failure != 'checksum' else b'changed').hexdigest()}}}
                with patch.object(installer.platform, 'system', return_value='Linux'), \
                        patch.object(installer.platform, 'machine', return_value='x86_64'), \
                        patch('sys.argv', ['install.py', '--repo', '/test/repo']), \
                        patch.object(installer, 'download', side_effect=[json.dumps(channel).encode(), archive]) as download, \
                        patch.object(installer, 'extract_binary', return_value=b'fixture binary'), \
                        patch.object(installer.subprocess, 'check_output', return_value=b'{"managed_protocol":2}'), \
                        patch.object(installer.subprocess, 'run') as run:
                    if failure is None:
                        installer.main()
                        self.assertEqual(run.call_args.args[0][1:], ['install', '--runtime', '--repo', '/test/repo'])
                    else:
                        with self.assertRaises(ValueError):
                            installer.main()
                        run.assert_not_called()
                    expected_calls = [(installer.STABLE_CHANNEL, 1024 * 1024)]
                    if failure != 'version':
                        expected_calls.append((asset_url + '?download=1', installer.MAX_ARCHIVE))
                    self.assertEqual([call.args for call in download.call_args_list], expected_calls)
                    self.assertNotIn('api.github.com', installer.STABLE_CHANNEL)

    def test_archive_accepts_only_a_regular_executable(self):
        def archive(name='./doomer', kind=tarfile.REGTYPE, extra=False):
            data = io.BytesIO()
            with tarfile.open(fileobj=data, mode='w:gz') as tar:
                member = tarfile.TarInfo(name)
                member.type = kind
                member.mode = 0o755
                member.size = 3 if kind == tarfile.REGTYPE else 0
                member.linkname = '/tmp/untrusted'
                tar.addfile(member, io.BytesIO(b'bin') if member.size else None)
                if extra:
                    tar.addfile(tarfile.TarInfo('unexpected'))
            return data.getvalue()
        self.assertEqual(installer.extract_binary(archive()), b'bin')
        for data in [archive('../doomer'), archive(kind=tarfile.SYMTYPE), archive(extra=True)]:
            with self.assertRaises(ValueError):
                installer.extract_binary(data)

    def test_archive_accepts_the_published_documentation_layout(self):
        data = io.BytesIO()
        with tarfile.open(fileobj=data, mode='w:gz') as tar:
            for name in ['./', './docs/']:
                member = tarfile.TarInfo(name)
                member.type = tarfile.DIRTYPE
                tar.addfile(member)
            for name in ['./LICENSE', './README.md', './docs/release.md', './docs/trust-model.md', './doomer']:
                member = tarfile.TarInfo(name)
                member.mode = 0o755 if name == './doomer' else 0o644
                member.size = 3
                tar.addfile(member, io.BytesIO(b'bin'))
        self.assertEqual(installer.extract_binary(data.getvalue()), b'bin')


if __name__ == '__main__':
    unittest.main()
