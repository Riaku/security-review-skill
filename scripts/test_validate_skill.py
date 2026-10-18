import subprocess
import unittest
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestSkill(unittest.TestCase):
    def run_validator(self, *flags):
        return subprocess.run(
            ["python3", str(ROOT / "scripts" / "validate_skill.py"), *flags],
            capture_output=True, text=True)

    def test_passes_on_complete_tree(self):
        r = self.run_validator()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("OK:", r.stdout)


if __name__ == "__main__":
    unittest.main()
