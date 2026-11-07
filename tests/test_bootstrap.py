import hashlib
import importlib.util
import io
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
        text = (ROOT / 'skills/doomer-review/SKILL.md').read_text()
        self.assertIn('doomer-protocol: "2"', text)
        self.assertIn('doomer-update-policy: stable', text)
        self.assertIn('doomer prepare', text)
        self.assertIn('doomer prepare --task HANDLE', text)
        self.assertIn('doomer task repair HANDLE', text)
        self.assertLess(len(text), 8192)
        self.assertNotIn('self-update', text)
        self.assertNotIn('doomer-version:', text)
        self.assertIn('doomer-cli-range:', text)
        self.assertNotIn('/main/INSTALL.md', text)
        self.assertRegex(text, r'skills/[a-f0-9]{40}/INSTALL.md')
        self.assertIn(hashlib.sha256((ROOT / 'INSTALL.md').read_bytes()).hexdigest(), text)
        self.assertFalse((ROOT / 'skills/doomer-review/references').exists())

    def test_installer_is_pinned_and_scope_requires_a_choice(self):
        guide = (ROOT / 'INSTALL.md').read_text()
        self.assertRegex(guide, r'skills/[a-f0-9]{40}/scripts/install.py')
        self.assertIn(hashlib.sha256((ROOT / 'scripts/install.py').read_bytes()).hexdigest(), guide)
        self.assertIn('ask personal versus team and wait', guide)
        self.assertIn('returns another protocol', guide)

    def test_macos_download_loads_system_ca_bundle(self):
        context = MagicMock(check_hostname=True, verify_mode=ssl.CERT_REQUIRED)
        response = MagicMock()
        response.url = 'https://example.invalid/file'
        response.read.return_value = b'verified'
        response.__enter__.return_value = response
        with patch.object(installer.platform, 'system', return_value='Darwin'), \
                patch.object(installer.ssl, 'create_default_context', return_value=context), \
                patch.object(installer.Path, 'is_file', return_value=True), \
                patch.dict(installer.os.environ, {}, clear=True), \
                patch.object(installer.urllib.request, 'urlopen', return_value=response) as open_url:
            self.assertEqual(installer.download(response.url, 100), b'verified')
            context.load_verify_locations.assert_called_once_with(cafile='/etc/ssl/cert.pem')
            self.assertIs(open_url.call_args.kwargs['context'], context)
            self.assertTrue(context.check_hostname)
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)

    def test_explicit_ca_bundle_is_preserved(self):
        context = MagicMock(check_hostname=True, verify_mode=ssl.CERT_REQUIRED)
        response = MagicMock()
        response.url = 'https://example.invalid/file'
        response.read.return_value = b'verified'
        response.__enter__.return_value = response
        with patch.object(installer.platform, 'system', return_value='Darwin'), \
                patch.object(installer.ssl, 'create_default_context', return_value=context), \
                patch.dict(installer.os.environ, {'SSL_CERT_FILE': '/custom/roots.pem'}, clear=True), \
                patch.object(installer.urllib.request, 'urlopen', return_value=response) as open_url:
            installer.download(response.url, 100)
            context.load_verify_locations.assert_not_called()
            self.assertIs(open_url.call_args.kwargs['context'], context)
            self.assertTrue(context.check_hostname)
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)

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
