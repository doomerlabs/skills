import importlib.util
from pathlib import Path
import unittest
import subprocess
import sys
import tempfile

spec = importlib.util.spec_from_file_location('stage_managed', Path(__file__).parents[1] / 'scripts/stage-managed-skill.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ManagedSkillTests(unittest.TestCase):
    def test_frontmatter_is_preserved(self):
        raw = b'---\nname: doomer-review\n---\nbody\n'
        marked = module.render(raw, 'skills/doomer-review/SKILL.md', 'a' * 40)
        self.assertTrue(marked.startswith(b'---\nname: doomer-review\n---\n<!-- doomer-managed\n'))
        self.assertEqual(marked.split(b'-->\n', 1)[1], b'body\n')

    def test_source_revision_and_path(self):
        marked = module.render(b'content\n', 'skills/doomer-review/references/install.md', 'b' * 40)
        self.assertIn(b'revision: ' + b'b' * 40, marked)
        self.assertIn(b'source: skills/doomer-review/references/install.md\n', marked)
        self.assertTrue(marked.endswith(b'-->\ncontent\n'))

    def test_reject_invalid_frontmatter_and_revision(self):
        with self.assertRaises(ValueError):
            module.render(b'body', 'skills/doomer-review/SKILL.md', 'a' * 40)
        with self.assertRaises(ValueError):
            module.render(b'body', 'skills/doomer-review/references/install.md', '../main')

    def test_stage_checks_complete_inventory_and_preserves_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "skills/doomer-review"
            (source / "references").mkdir(parents=True)
            (source / "SKILL.md").write_bytes(b"---\nname: doomer-review\n---\nbody\n")
            for name in ("install.md", "updates.md"):
                (source / "references" / name).write_bytes(b"reference\n")
            def git(*args):
                return subprocess.check_output(
                    ["git", "-C", str(root), "-c", "core.hooksPath=/dev/null",
                     "-c", "user.name=Test", "-c", "user.email=test@example.com", *args],
                    stderr=subprocess.DEVNULL, text=True,
                ).strip()
            git("init")
            git("add", ".")
            git("commit", "-m", "source")
            revision = git("rev-parse", "HEAD")
            target = root / "staged"
            module.stage(root, target, revision)
            self.assertIn(revision.encode(), (target / "SKILL.md").read_bytes())
            self.assertNotIn(b"doomer-managed", (source / "SKILL.md").read_bytes())
            with self.assertRaises(FileExistsError):
                module.stage(root, target, revision)
            (source / "references/install.md").unlink()
            with self.assertRaises(ValueError):
                module.stage(root, root / "missing-file", revision)
            (source / "references/install.md").symlink_to(target / "references/install.md")
            with self.assertRaises(ValueError):
                module.stage(root, root / "symlink", revision)


    def test_both_agents_cli_stages_identical_regular_trees(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "skills/doomer-review"
            (source / "references").mkdir(parents=True)
            (source / "SKILL.md").write_bytes(b"---\nname: doomer-review\n---\nboth agents\n")
            for name in ("install.md", "updates.md"):
                (source / "references" / name).write_bytes(b"reference\n")
            # An additional non-Markdown resource must be copied to both too.
            (source / "resource.bin").write_bytes(b"\x00\xff")
            def git(*args):
                return subprocess.check_output(
                    ["git", "-C", str(root), "-c", "core.hooksPath=/dev/null",
                     "-c", "user.name=Test", "-c", "user.email=test@example.com", *args],
                    stderr=subprocess.DEVNULL, text=True,
                ).strip()
            git("init")
            git("add", ".")
            git("commit", "-m", "source")
            for version in ("old", "new"):
                if version == "new":
                    (source / "references/install.md").write_bytes(b"updated pin\n")
                    git("add", "skills")
                    git("commit", "-m", "update")
                revision = git("rev-parse", "HEAD")
                target = root / version
                subprocess.run([sys.executable, module.__file__, str(root), revision,
                                str(target), "--both-agents"], check=True)
                codex, claude = (target / path for path in module.PROJECT_SKILL_PATHS)
                inventory = lambda path: {p.relative_to(path).as_posix(): p.read_bytes()
                                          for p in path.rglob("*") if p.is_file()}
                self.assertEqual(inventory(codex), inventory(claude))
                self.assertEqual(set(inventory(codex)),
                                 {"SKILL.md", "references/install.md", "references/updates.md", "resource.bin"})
                self.assertIn(revision.encode(), (codex / "SKILL.md").read_bytes())
                for path in target.rglob("*"):
                    self.assertFalse(path.is_symlink())
                single = root / (version + "-single")
                subprocess.run([sys.executable, module.__file__, str(root), revision,
                                str(single)], check=True)
                self.assertEqual(inventory(single), inventory(codex))
                self.assertFalse((single / ".agents").exists())
                self.assertFalse((single / ".claude").exists())
                before = inventory(codex)
                with self.assertRaises(FileExistsError):
                    module.stage(root, target, revision, both_agents=True)
                self.assertEqual(inventory(codex), before)
            self.assertNotEqual(inventory(root / "old" / module.PROJECT_SKILL_PATHS[0]),
                                inventory(root / "new" / module.PROJECT_SKILL_PATHS[0]))
            self.assertNotIn(b"doomer-managed", (source / "SKILL.md").read_bytes())
            (source / "references/install.md").write_bytes(b"uncommitted modification\n")
            with self.assertRaises(ValueError):
                module.stage(root, root / "invalid", revision, both_agents=True)
            self.assertFalse((root / "invalid").exists())


if __name__ == '__main__':
    unittest.main()
