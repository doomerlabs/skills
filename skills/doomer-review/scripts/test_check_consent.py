import base64
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import check_consent as consent


class ConsentTests(unittest.TestCase):
    def test_requires_matching_saved_browser_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = Path('/test/repo')
            common = repo / '.git'
            self.assertFalse(consent.check(repo, common, base)['approved'])
            state = base / 'watch' / hashlib.sha256((consent.API + '\0' + consent.PROFILE).encode()).hexdigest()
            state.mkdir(parents=True)
            token = 'doomer_anon_' + base64.urlsafe_b64encode(bytes(range(32))).decode().rstrip('=')
            config = dict(version=1, explicit_consent=True, api_url=consent.API,
                          profile=consent.PROFILE, consented_at='2026-10-30T00:00:00Z',
                          directories=[str(repo)], account_key=hashlib.sha256(token.encode()).hexdigest())
            (state / 'anonymous.json').write_text(json.dumps(dict(Token=token, API=consent.API, Profile=consent.PROFILE)))
            def save():
                (state / 'config.json').write_text(json.dumps(config))
            save()
            self.assertTrue(consent.check(repo, common, base)['approved'])
            self.assertFalse(consent.check(Path('/other/repo'), Path('/other/repo/.git'), base)['approved'])
            config['explicit_consent'] = False
            save()
            self.assertFalse(consent.check(repo, common, base)['approved'])
            config['explicit_consent'] = True
            config['account_key'] = 'different-account'
            save()
            self.assertFalse(consent.check(repo, common, base)['approved'])

    def test_localhost_approval_does_not_authorize_production(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = Path('/test/repo')
            state = base / 'watch' / hashlib.sha256(b'http://localhost:3000/api\0skill-dev').hexdigest()
            state.mkdir(parents=True)
            (state / 'config.json').write_text(json.dumps(dict(
                version=1, explicit_consent=True, api_url='http://localhost:3000/api',
                profile='skill-dev', consented_at='2026-11-02T00:00:00Z', directories=[str(repo)])))
            self.assertFalse(consent.check(repo, repo / '.git', base)['approved'])


if __name__ == '__main__':
    unittest.main()
