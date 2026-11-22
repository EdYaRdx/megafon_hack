from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POWERSHELL = shutil.which("powershell") or shutil.which("pwsh")

# Only the external command adapters are replaced. The real selection, import
# probe protocol, returned-executable verification, JSON and exit status run in PS.
ADAPTER = r'''
param([Alias('Python')][string]$RequestedPython)
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
. (Join-Path $PSScriptRoot 'tools/find_python.ps1')
$data = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'fixture.json') -Raw -Encoding UTF8 | ConvertFrom-Json
function Get-DiscoveryApplications {
    param([string]$Name)
    $entry = $data.commands.PSObject.Properties[$Name]
    if ($null -ne $entry) { $entry.Value }
}
function Invoke-DiscoveryProcess {
    param([string]$Executable, [string[]]$Arguments, [int]$TimeoutMilliseconds = 5000)
    $event = [pscustomobject]@{ executable = $Executable; arguments = @($Arguments) }
    [IO.File]::AppendAllText((Join-Path $PSScriptRoot 'calls.jsonl'), (($event | ConvertTo-Json -Compress) + "`n"))
    $entry = $data.programs.PSObject.Properties[$Executable]
    $program = $null
    if ($null -ne $entry) { $program = $entry.Value }
    $failure = [pscustomobject]@{ ExitCode = 1; Stdout = ''; Stderr = 'Unknown fixture command.' }
    if ($null -eq $program) { return $failure }
    if ($program.kind -eq 'py') {
        if ($Arguments.Count -eq 1 -and $Arguments[0] -eq '-0p') {
            return [pscustomobject]@{ ExitCode = 0; Stdout = $program.listing; Stderr = '' }
        }
        $selection = $program.selections.PSObject.Properties[$Arguments[0]]
        if ($null -eq $selection) { return $failure }
        $program = $selection.Value
        $Arguments = @($Arguments | Select-Object -Skip 1)
    } elseif ($program.kind -eq 'uv') {
        if (($Arguments -join '|') -ne 'python|find|--no-project|--no-config|--no-python-downloads|--offline|>=3.12') { return $failure }
        return [pscustomobject]@{ ExitCode = 0; Stdout = $program.executable; Stderr = '' }
    }
    if ($program.kind -eq 'version-only') {
        if (($Arguments -join '|') -eq '--version') {
            return [pscustomobject]@{ ExitCode = 0; Stdout = 'Python 3.12.9'; Stderr = '' }
        }
        return [pscustomobject]@{ ExitCode = 1; Stdout = ''; Stderr = 'Fatal Python error: No module named encodings' }
    }
    if ($program.kind -ne 'python' -or $Arguments.Count -ne 2 -or $Arguments[0] -ne '-c') { return $failure }
    $payload = [pscustomobject]@{ executable = $program.executable; version = $program.version }
    [pscustomobject]@{ ExitCode = 0; Stdout = ($payload | ConvertTo-Json -Compress); Stderr = '' }
}
$result = Find-DiscoveryPython -Python $RequestedPython
$result | ConvertTo-Json -Depth 5 -Compress
if ($result.status -eq 'FOUND') { exit 0 }
exit 1
'''


@unittest.skipUnless(POWERSHELL, "PowerShell unavailable; no installation attempted")
class FindPythonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="python discovery ")
        self.addCleanup(self.temp.cleanup)
        # pathlib may resolve a Windows 8.3 temp alias to the long profile path.
        self.project = Path(self.temp.name).resolve()
        (self.project / "tools").mkdir()
        shutil.copyfile(ROOT / "tools" / "find_python.ps1", self.project / "tools" / "find_python.ps1")
        self.wrapper = self.project / "discover.ps1"
        self.wrapper.write_text(ADAPTER, encoding="utf-8")
        self.commands: dict[str, list[str]] = {}
        self.programs: dict[str, dict] = {}

    def executable(self, relative: str, kind: str = "python", version: str = "3.12.9") -> str:
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        absolute = str(path.resolve())
        self.programs[absolute] = {"kind": kind, "version": version, "executable": absolute}
        return absolute

    def run_ps(self, script: Path, *arguments: str, timeout: int = 30) -> subprocess.CompletedProcess:
        return subprocess.run(
            [POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(script), *arguments],
            cwd=self.project, capture_output=True, text=True, encoding="utf-8", timeout=timeout,
        )

    def discover(self, explicit: str | None = None) -> tuple[subprocess.CompletedProcess, dict]:
        (self.project / "fixture.json").write_text(
            json.dumps({"commands": self.commands, "programs": self.programs}), encoding="utf-8"
        )
        result = self.run_ps(self.wrapper, *(["-Python", explicit] if explicit is not None else []))
        self.assertEqual(result.stderr, "", result.stderr)
        return result, json.loads(result.stdout)

    def calls(self) -> list[dict]:
        path = self.project / "calls.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines()] if path.exists() else []

    def assert_found(self, result: subprocess.CompletedProcess, payload: dict, executable: str, source: str) -> None:
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(payload["status"], "FOUND")
        self.assertEqual(payload["executable"], executable)
        self.assertEqual(payload["source"], source)
        self.assertGreaterEqual(tuple(map(int, payload["version"].split("."))), (3, 12))
        self.assertTrue(payload["diagnostics"])

    def test_path_first_working_python_wins_over_other_sources(self) -> None:
        chosen = self.executable("installed/python.exe")
        other = self.executable("other/python.exe", version="3.14.0")
        self.commands = {"python": [chosen, other], "python3": [other]}
        self.executable(".venv/Scripts/python.exe")
        result, payload = self.discover()
        self.assert_found(result, payload, chosen, "PATH python")
        self.assertEqual(len(self.calls()), 1)

    def test_explicit_path_with_spaces_and_unicode_has_first_priority(self) -> None:
        chosen = self.executable("operator \u0442\u0435\u0441\u0442/python.exe")
        self.commands = {"python": [self.executable("installed/python.exe")]}
        result, payload = self.discover(chosen)
        self.assert_found(result, payload, chosen, "explicit")

    def test_wrong_explicit_path_is_diagnosed_then_falls_back(self) -> None:
        chosen = self.executable("installed/python3.exe")
        self.commands = {"python3": [chosen]}
        result, payload = self.discover(str(self.project / "missing.exe"))
        self.assert_found(result, payload, chosen, "PATH python3")
        self.assertIn("does not exist", payload["diagnostics"][0]["message"])

    def test_no_installed_options_returns_clear_stop(self) -> None:
        result, payload = self.discover()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "STOP")
        self.assertIsNone(payload["executable"])
        self.assertIn("No verified Python >=3.12", payload["message"])
        self.assertEqual(self.calls(), [])

    def test_store_alias_is_not_executed_and_local_venv_is_used(self) -> None:
        alias = self.executable("Microsoft/WindowsApps/python.exe", kind="version-only")
        chosen = self.executable(".venv/Scripts/python.exe")
        self.commands = {"python": [alias]}
        result, payload = self.discover()
        self.assert_found(result, payload, chosen, "project .venv")
        self.assertIn("Skipped Microsoft Store", payload["diagnostics"][0]["message"])
        self.assertNotIn(alias, [call["executable"] for call in self.calls()])

    def test_version_only_with_broken_stdlib_is_rejected(self) -> None:
        broken = self.executable("broken/python.exe", kind="version-only")
        chosen = self.executable("working/python3.exe")
        self.commands = {"python": [broken], "python3": [chosen]}
        result, payload = self.discover()
        self.assert_found(result, payload, chosen, "PATH python3")
        self.assertIn("encodings", payload["diagnostics"][0]["message"])

    def test_below_minimum_python_is_rejected(self) -> None:
        old = self.executable("old/python.exe", version="3.11.11")
        self.commands = {"python": [old]}
        result, payload = self.discover()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "STOP")
        self.assertIn("below required 3.12", payload["diagnostics"][0]["message"])

    def launcher(self, selections: dict, listing: str = "") -> str:
        launcher = self.executable("launcher/py.exe", kind="py")
        self.programs[launcher].update(selections=selections, listing=listing)
        self.commands["py"] = [launcher]
        return launcher

    def test_py_312_resolves_and_directly_verifies_executable(self) -> None:
        chosen = self.executable("Python312/python.exe")
        self.launcher({"-3.12": self.programs[chosen]})
        result, payload = self.discover()
        self.assert_found(result, payload, chosen, "py -3.12")
        self.assertEqual(self.calls()[-1]["executable"], chosen)

    def test_py_enumerates_newer_versions_in_descending_order(self) -> None:
        older = self.executable("Python313/python.exe", version="3.13.4")
        chosen = self.executable("Python314/python.exe", version="3.14.1")
        self.launcher(
            {"-V:3.13": self.programs[older], "-V:3.14": self.programs[chosen]},
            f" -V:3.11 * ignored\n -V:3.13 {older}\n -V:3.14 {chosen}\n",
        )
        result, payload = self.discover()
        self.assert_found(result, payload, chosen, "py -V:3.14")
        self.assertNotIn(older, [call["executable"] for call in self.calls()])

    def test_py_can_fall_back_across_multiple_installed_versions(self) -> None:
        broken = self.executable("Python314/python.exe", kind="version-only")
        chosen = self.executable("Python313/python.exe", version="3.13.8")
        self.launcher(
            {"-3.14-64": self.programs[broken], "-3.13-64": self.programs[chosen]},
            f" -3.13-64 * {chosen}\n -3.14-64 {broken}\n",
        )
        result, payload = self.discover()
        self.assert_found(result, payload, chosen, "py -3.13-64")
        self.assertTrue(any("encodings" in item["message"] for item in payload["diagnostics"]))

    def test_launcher_claim_is_not_enough_if_exact_executable_is_broken(self) -> None:
        broken = self.executable("unusable/python.exe", kind="version-only")
        self.launcher({"-3.12": {"kind": "python", "executable": broken, "version": "3.12.9"}})
        result, payload = self.discover()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "STOP")
        self.assertTrue(any("Direct executable probe failed" in item["message"] for item in payload["diagnostics"]))

    def test_uv_uses_only_installed_offline_interpreter(self) -> None:
        chosen = self.executable("uv installed \u0442\u0435\u0441\u0442/python.exe", version="3.14.0")
        uv = self.executable("uv/uv.exe", kind="uv")
        self.programs[uv]["executable"] = chosen
        self.commands = {"uv": [uv]}
        result, payload = self.discover()
        self.assert_found(result, payload, chosen, "uv python find")

    def test_broken_py312_falls_back_to_working_offline_uv(self) -> None:
        broken = self.executable("broken312/python.exe", kind="version-only")
        launcher = self.launcher({"-3.12": self.programs[broken]})
        chosen = self.executable("uv installed/python.exe")
        uv = self.executable("uv/uv.exe", kind="uv")
        self.programs[uv]["executable"] = chosen
        self.commands["uv"] = [uv]
        result, payload = self.discover()
        self.assert_found(result, payload, chosen, "uv python find")
        calls = self.calls()
        self.assertIn(launcher, [call["executable"] for call in calls])
        self.assertIn("encodings", str(payload["diagnostics"]))
        self.assertEqual(calls[-1]["executable"], chosen)

    def test_attempt_count_is_bounded(self) -> None:
        self.commands = {"python": [self.executable(f"bad{i}/python.exe", kind="version-only") for i in range(30)]}
        launcher = self.launcher({})
        result, payload = self.discover()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "STOP")
        self.assertLessEqual(len(self.calls()), 24)
        self.assertNotIn(launcher, [call["executable"] for call in self.calls()])
        self.assertTrue(any("safety limit" in item["message"] for item in payload["diagnostics"]))

    def test_real_process_adapter_preserves_spaced_unicode_and_quoted_arguments(self) -> None:
        child = self.project / "child \u0442\u0435\u0441\u0442.ps1"
        child.write_text("param([string]$Value)\n[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)\n@{value=$Value} | ConvertTo-Json -Compress\n", encoding="utf-8")
        value = 'spaces \u0442\u0435\u0441\u0442 "quoted" trailing\\'
        config = self.project / "process.json"
        config.write_text(json.dumps({"executable": POWERSHELL, "script": str(child), "value": value}), encoding="utf-8")
        driver = self.project / "process.ps1"
        driver.write_text(r'''
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
. (Join-Path $PSScriptRoot 'tools/find_python.ps1')
$c = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'process.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$r = Invoke-DiscoveryProcess -Executable $c.executable -Arguments @('-NoLogo', '-NoProfile', '-NonInteractive', '-File', $c.script, '-Value', $c.value)
$r | ConvertTo-Json -Compress
''', encoding="utf-8")
        result = self.run_ps(driver)
        self.assertEqual(result.returncode, 0, result.stderr)
        outcome = json.loads(result.stdout)
        self.assertEqual(outcome["ExitCode"], 0, outcome)
        self.assertEqual(json.loads(outcome["Stdout"])["value"], value)

    def test_real_process_adapter_times_out(self) -> None:
        child = self.project / "sleep.ps1"
        child.write_text("Start-Sleep -Seconds 20\n", encoding="utf-8")
        config = self.project / "process.json"
        config.write_text(json.dumps({"executable": POWERSHELL, "script": str(child)}), encoding="utf-8")
        driver = self.project / "timeout.ps1"
        driver.write_text(r'''
. (Join-Path $PSScriptRoot 'tools/find_python.ps1')
$c = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'process.json') -Raw -Encoding UTF8 | ConvertFrom-Json
Invoke-DiscoveryProcess -Executable $c.executable -Arguments @('-NoProfile', '-NonInteractive', '-File', $c.script) -TimeoutMilliseconds 200 | ConvertTo-Json -Compress
''', encoding="utf-8")
        result = self.run_ps(driver, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        outcome = json.loads(result.stdout)
        self.assertNotEqual(outcome["ExitCode"], 0)
        self.assertIn("Timed out", outcome["Stderr"])

    @unittest.skipUnless(sys.version_info >= (3, 12), "requires supported test-runner Python")
    def test_real_cli_verifies_running_python_without_discovery_mocks(self) -> None:
        result = self.run_ps(self.project / "tools" / "find_python.ps1", "-Python", sys.executable)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assert_found(result, payload, str(Path(sys.executable).resolve()), "explicit")

    def test_real_probe_does_not_hide_invalid_inherited_io_encoding(self) -> None:
        config = self.project / "environment.json"
        config.write_text(json.dumps({"executable": sys.executable}), encoding="utf-8")
        driver = self.project / "environment.ps1"
        driver.write_text(r'''
. (Join-Path $PSScriptRoot 'tools/find_python.ps1')
function Get-DiscoveryApplications { param([string]$Name) @() }
$c = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'environment.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$r = Find-DiscoveryPython -Python $c.executable
$r | ConvertTo-Json -Depth 5 -Compress
if ($r.status -eq 'FOUND') { exit 0 }
exit 1
''', encoding="utf-8")
        environment = dict(os.environ, PYTHONIOENCODING="nonexistent-encoding-for-discovery-test")
        result = subprocess.run(
            [POWERSHELL, "-NoProfile", "-NonInteractive", "-File", str(driver)],
            cwd=self.project, env=environment, capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        payload = json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "STOP")
        self.assertTrue(any("probe failed" in item["message"] for item in payload["diagnostics"]))

    @unittest.skipUnless(sys.version_info >= (3, 12), "requires supported test-runner Python")
    def test_real_relative_explicit_path_uses_powershell_location(self) -> None:
        executable = Path(sys.executable).resolve()
        config = self.project / "relative.json"
        config.write_text(json.dumps({"directory": str(executable.parent), "name": executable.name}), encoding="utf-8")
        driver = self.project / "relative.ps1"
        driver.write_text(r'''
. (Join-Path $PSScriptRoot 'tools/find_python.ps1')
$c = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'relative.json') -Raw -Encoding UTF8 | ConvertFrom-Json
Set-Location -LiteralPath $c.directory
$r = Find-DiscoveryPython -Python (Join-Path '.' $c.name)
$r | ConvertTo-Json -Depth 5 -Compress
if ($r.status -eq 'FOUND') { exit 0 }
exit 1
''', encoding="utf-8")
        result = self.run_ps(driver)
        self.assert_found(result, json.loads(result.stdout), str(executable), "explicit")

    def test_real_process_uses_changed_powershell_working_directory(self) -> None:
        location = self.project / "new working directory"
        location.mkdir()
        config = self.project / "location.json"
        config.write_text(json.dumps({"directory": str(location), "executable": sys.executable}), encoding="utf-8")
        driver = self.project / "location.ps1"
        driver.write_text(r'''
. (Join-Path $PSScriptRoot 'tools/find_python.ps1')
$c = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'location.json') -Raw -Encoding UTF8 | ConvertFrom-Json
Set-Location -LiteralPath $c.directory
$r = Invoke-DiscoveryProcess -Executable $c.executable -Arguments @('-c', 'import json,os; print(json.dumps({"cwd":os.getcwd()}))')
$r | ConvertTo-Json -Compress
''', encoding="utf-8")
        result = self.run_ps(driver)
        outcome = json.loads(result.stdout)
        self.assertEqual(outcome["ExitCode"], 0, outcome)
        self.assertEqual(Path(json.loads(outcome["Stdout"])["cwd"]), location)


if __name__ == "__main__":
    unittest.main()
