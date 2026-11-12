import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_pinned_bootstrap", ROOT / "scripts/verify_pinned_bootstrap.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class PinnedBootstrapVerificationTest(unittest.TestCase):
    def setUp(self):
        self.skill = (ROOT / "skills/doomer-review/SKILL.md").read_text()
        self.version = "2026.11.10.3"

    def test_normalizes_only_the_reviewed_policy_fields(self):
        result = verifier.stable_verification_copy(self.skill, self.version)
        self.assertEqual(result.split("\n---\n", 1)[1], self.skill.split("\n---\n", 1)[1])
        self.assertIn("  doomer-update-policy: stable\n", result)
        self.assertIn("  doomer-cli-range: '>=2026.11.10.3'\n", result)
        self.assertNotIn("  doomer-version:", result)

    def test_rejects_wrong_pin_policy_range_or_duplicate_fields(self):
        for original, changed in [
            ("doomer-version: 2026.11.10.3", "doomer-version: 2026.11.10.4"),
            ("doomer-update-policy: pinned", "doomer-update-policy: stable"),
            ("doomer-cli-range: '=2026.11.10.3'", "doomer-cli-range: '>=2026.11.10.3'"),
            ("  doomer-version: 2026.11.10.3", "  doomer-version: 2026.11.10.3\n  doomer-version: 2026.11.10.3"),
        ]:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                verifier.stable_verification_copy(self.skill.replace(original, changed, 1), self.version)

    def test_preserves_other_changes_for_the_canonical_verifier_to_reject(self):
        altered = self.skill.replace("# Doomer review", "# Different instructions", 1)
        result = verifier.stable_verification_copy(altered, self.version)
        self.assertIn("# Different instructions", result)


if __name__ == "__main__":
    unittest.main()
