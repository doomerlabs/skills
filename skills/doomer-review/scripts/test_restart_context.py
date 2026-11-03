import json
from pathlib import Path
import tempfile
import unittest

from restart_context import restart_context


class RestartContextTests(unittest.TestCase):
    def test_consumes_once_and_preserves_other_agent_instructions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / 'repo'
            repo.mkdir()
            agents = repo / 'AGENTS.md'
            original = '# Existing rules\nKeep these rules.\n'
            agents.write_text(original)
            base = root / 'config'
            self.assertEqual(restart_context(base, repo, 'session', 'Add pagination')['status'], 'restart_context_saved')
            self.assertIn('Resume after doomer.ai setup', agents.read_text())
            self.assertEqual(restart_context(base, repo, 'other')['status'], 'restart_context_unavailable')
            self.assertIn('Resume after doomer.ai setup', agents.read_text())
            result = restart_context(base, repo, 'session')
            self.assertEqual(result['original_request'], 'Add pagination')
            self.assertEqual(agents.read_text(), original)
            self.assertEqual(restart_context(base, repo, 'session')['status'], 'restart_context_unavailable')

    def test_old_and_wrong_repository_context_are_not_consumed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / 'repo'
            repo.mkdir()
            base = root / 'config'
            restart_context(base, repo, 'session', 'Original request')
            file = next((base / 'onboarding').glob('*.json'))
            data = json.loads(file.read_text())
            for update in [{'created': 0}, {'repo': str(root / 'other')}]:
                file.write_text(json.dumps(dict(data, **update)))
                self.assertEqual(restart_context(base, repo, 'session')['status'], 'restart_context_unavailable')
                self.assertTrue(file.exists())
            file.write_text(json.dumps(data))
            self.assertEqual(restart_context(base, repo, 'session')['status'], 'restart_context_consumed')


if __name__ == '__main__':
    unittest.main()
