from __future__ import annotations

import base64
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import venv

ROOT = Path(__file__).resolve().parents[1]
POWERSHELL = shutil.which('powershell')


@unittest.skipUnless(os.name == 'nt' and POWERSHELL, 'Requires Windows PowerShell execution-policy semantics')
class RuntimeFallbackTests(unittest.TestCase):
    def run_fallback(self, candidates: list[str], *, utf8_discovery: bool = False) -> dict:
        # Execute the actual documented inline block, not a second implementation.
        section = (ROOT / 'prompts/first-run.md').read_text(encoding='utf-8').split(
            '## Рабочий Python для файловых команд', 1
        )[1].split('\n## ', 1)[0]
        blocks = re.findall(r'```powershell\n(.*?)\n```', section, re.S)
        probe = next(block for block in blocks if block.startswith('$Python = $null'))
        console_setup = next(block for block in blocks if block.startswith('[Console]::OutputEncoding'))
        locator = r'''
    $Candidate = & $Candidate -c 'import sys; sys.stdout.buffer.write(sys.executable.encode())'
    if ($LASTEXITCODE -ne 0) { throw 'Fixture native lookup failed' }
''' if utf8_discovery else ''
        with tempfile.TemporaryDirectory(prefix='runtime fallback ') as folder:
            root = Path(folder)
            blocked = root / 'blocked.ps1'
            marker = root / 'must-not-exist'
            blocked.write_text("Set-Content -LiteralPath 'must-not-exist' -Value executed\n", encoding='utf-8')
            config = root / 'candidates.json'
            config.write_text(json.dumps(candidates), encoding='utf-8')
            # Restricted tightens only this child's Process scope. No persistent
            # policy is changed; domain policy retains precedence. Inline -Command
            # remains permitted by this synthetic script-file-only restriction.
            script = r'''
$ErrorActionPreference = 'Stop'
$Blocked = $false
try { & ./blocked.ps1 } catch [System.Management.Automation.PSSecurityException] { $Blocked = $true }
if (-not $Blocked) { throw 'Fixture did not block PS1; higher-scope policy may override Process' }
$Candidates = Get-Content -LiteralPath ./candidates.json -Raw | ConvertFrom-Json
# Force a legacy decoder so the Unicode case cannot pass via inherited UTF-8.
[Console]::OutputEncoding = [System.Text.Encoding]::GetEncoding(437)
''' + console_setup + r'''
$Attempts = 0
$Selected = $null
foreach ($Candidate in $Candidates) {
    $Attempts++
''' + locator + probe + r'''
    if ($null -ne $Python) { $Selected = $Python; break }
}
@{blocked=$Blocked; executable=$Selected; attempts=$Attempts; status=$(if ($Selected) {'FOUND'} else {'STOP'}); processPolicy=(Get-ExecutionPolicy -Scope Process).ToString()} | ConvertTo-Json -Compress
'''
            encoded = base64.b64encode(script.encode('utf-16-le')).decode('ascii')
            result = subprocess.run(
                [POWERSHELL, '-NoLogo', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Restricted', '-EncodedCommand', encoded],
                cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=20,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists(), 'Blocked script executed')
            payload = json.loads(result.stdout.splitlines()[-1])
            self.assertTrue(payload['blocked'])
            self.assertEqual(payload['processPolicy'], 'Restricted')
            return payload

    @unittest.skipUnless(sys.version_info >= (3, 12), 'Requires already installed Python >=3.12')
    def test_blocked_ps1_still_allows_documented_native_probe(self) -> None:
        payload = self.run_fallback([sys.executable])
        self.assertEqual(payload['status'], 'FOUND')
        self.assertEqual(Path(payload['executable']).resolve(), Path(sys.executable).resolve())

    @unittest.skipUnless(sys.version_info >= (3, 12), 'Requires already installed Python >=3.12')
    def test_utf8_native_discovery_preserves_unicode_interpreter_path(self) -> None:
        with tempfile.TemporaryDirectory(prefix='unicode discovery ') as folder:
            environment = Path(folder) / 'installed \u0442\u0435\u0441\u0442'
            venv.EnvBuilder(with_pip=False).create(environment)
            executable = environment / 'Scripts' / 'python.exe'
            payload = self.run_fallback([str(executable)], utf8_discovery=True)
            self.assertEqual(payload['status'], 'FOUND')
            self.assertEqual(Path(payload['executable']).resolve(), executable.resolve())

    def test_all_offered_native_executables_refused_stops(self) -> None:
        with tempfile.TemporaryDirectory(prefix='denied native ') as folder:
            # Existing non-PE .exe files force an actual native process launch
            # refusal, without ACL/global policy changes or mocked PS commands.
            candidates = [Path(folder) / 'denied-one.exe', Path(folder) / 'denied-two.exe']
            for candidate in candidates:
                candidate.write_bytes(b'This synthetic file is not a native executable.\n')
            payload = self.run_fallback([str(path) for path in candidates])
        self.assertEqual(payload['status'], 'STOP')
        self.assertIsNone(payload['executable'])
        self.assertEqual(payload['attempts'], 2)


if __name__ == '__main__':
    unittest.main()
