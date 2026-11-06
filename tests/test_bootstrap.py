import importlib.util
import io
from pathlib import Path
import tarfile
import unittest

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
        self.assertLess(len(text), 2500)
        self.assertNotIn('self-update', text)
        self.assertNotIn('2026.', text)
        self.assertFalse((ROOT / 'skills/doomer-review/references').exists())

    def test_archive_accepts_only_a_regular_executable(self):
        def archive(name='./doomer', kind=tarfile.REGTYPE, extra=False):
            data = io.BytesIO()
            with tarfile.open(fileobj=data, mode='w:gz') as tar:
                member = tarfile.TarInfo(name)
                member.type = kind
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


if __name__ == '__main__':
    unittest.main()
