import json
from pathlib import Path
import tempfile
import unittest

from check_review import check, key, review_link


class ReviewTests(unittest.TestCase):
    def test_current_prompt_required_and_old_review_cannot_satisfy_new_turn(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = Path('/example/repo')
            def save(folder, name, value):
                p = root / folder / (key(name) + '.json')
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(json.dumps(value))
            self.assertEqual(check(root, repo, '')['status'], 'session_unknown')
            self.assertEqual(check(root, repo, 'session')['status'], 'prompt_not_captured')
            owner = {'session': 'session', 'turn': 'current'}
            save('turns', 'session', {'Owner': owner, 'Prompt': 'Make a change'})
            self.assertEqual(check(root, repo, 'session'), {'status': 'prompt_captured', 'turn': 'current'})
            self.assertEqual(check(root, repo, 'session', 'older')['status'], 'turn_changed')
            save('repositories', str(repo), {'Owner': owner, 'Fingerprint': 'new', 'HypothesesSubmitted': True})
            save('reviews', str(repo), {'Owner': {'session': 'session', 'turn': 'older'}, 'Fingerprint': 'new', 'AssessmentStatus': 'ready'})
            self.assertEqual(check(root, repo, 'session', 'current')['status'], 'assessment_pending')
            save('reviews', str(repo), {'Owner': owner, 'Fingerprint': 'old', 'AssessmentStatus': 'ready'})
            self.assertEqual(check(root, repo, 'session', 'current')['status'], 'assessment_pending')
            save('reviews', str(repo), {'Owner': owner, 'Fingerprint': 'new', 'AssessmentStatus': 'ready', 'ReviewID': 'review', 'Leads': []})
            self.assertEqual(check(root, repo, 'session', 'current')['status'], 'assessment_ready')
            save('reviews', str(repo), {'Owner': owner, 'Fingerprint': 'new', 'AssessmentStatus': 'unavailable'})
            self.assertEqual(check(root, repo, 'session', 'current')['status'], 'assessment_unavailable')
            save('repositories', str(repo), {'Owner': owner, 'Fingerprint': 'new', 'Ambiguous': True})
            self.assertEqual(check(root, repo, 'session', 'current')['status'], 'ownership_ambiguous')

    def test_pending_findings_reported_without_disclosing_feedback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = Path('/example/repo')
            owner = {'session': 'session', 'turn': 'current'}
            for folder, name, value in [
                ('turns', 'session', {'Owner': owner, 'Prompt': 'private prompt', 'Pending': [{'ReviewID': 'review'}]}),
                ('repositories', str(repo), {'Owner': owner, 'Fingerprint': 'new'}),
                ('reviews', str(repo), {'Owner': owner, 'Fingerprint': 'new', 'AssessmentStatus': 'ready', 'ReviewID': 'review', 'URL': 'private token', 'Leads': [{'Concern': 'private finding'}]})]:
                p = root / folder / (key(name) + '.json')
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(json.dumps(value))
            result = check(root, repo, 'session', 'current')
            self.assertEqual(result['pending_responses'], 1)
            self.assertEqual(result['lead_count'], 1)
            self.assertEqual(result['status'], 'feedback_pending')
            self.assertNotIn('private', json.dumps(result))

    def test_explicit_link_preserves_capability_and_rejects_other_sessions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = Path('/example/repo')
            path = root / 'reviews' / (key(str(repo)) + '.json')
            path.parent.mkdir(parents=True)
            url = 'https://doomer.ai/look-closer/org/repo/' + 'a' * 64
            private = url + '#review=' + 'A' * 43 + '&claim=' + 'B' * 43
            feed = {'Owner': {'session': 'original', 'turn': 'completed'},
                    'Anonymous': True, 'URL': private, 'ReviewID': 'review'}
            path.write_text(json.dumps(feed))
            self.assertEqual(review_link(root, repo, 'original')['url'], private)
            self.assertFalse(review_link(root, repo, 'original')['requires_sign_in'])
            self.assertNotIn('url', review_link(root, repo, 'different'))
            for invalid in [url, private.replace('doomer.ai', 'evil.example'), 'not a URL']:
                feed['URL'] = invalid
                path.write_text(json.dumps(feed))
                self.assertNotIn('url', review_link(root, repo, 'original'))
            feed.update(Anonymous=False, URL=url)
            path.write_text(json.dumps(feed))
            self.assertEqual(review_link(root, repo, 'original')['url'], url)
            self.assertTrue(review_link(root, repo, 'original')['requires_sign_in'])


if __name__ == '__main__':
    unittest.main()
