"""Release packager must never create output through an alias into its source."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.export_contest_demo import export


class ExportContainmentTests(unittest.TestCase):
    def test_destination_parent_alias_into_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            marker = source / "untouched.txt"
            marker.write_bytes(b"original source")
            alias = root / "alias"
            if sys.platform == "win32":
                result = subprocess.run(
                    ["cmd", "/d", "/c", "mklink", "/J", str(alias), str(source)],
                    capture_output=True,
                )
                if result.returncode:
                    self.skipTest("Windows junction creation is unavailable")
            else:
                alias.symlink_to(source, target_is_directory=True)
            try:
                with self.assertRaisesRegex(ValueError, "must not be inside its source"):
                    export(source, alias / "derived")
                self.assertEqual(list(source.iterdir()), [marker])
                self.assertEqual(marker.read_bytes(), b"original source")
            finally:
                if sys.platform == "win32":
                    alias.rmdir()
                else:
                    alias.unlink()


if __name__ == "__main__":
    unittest.main()
