# PowerShell 5.1 bootstrap; no Python, profile, downloads, or machine changes required.
[CmdletBinding()]
param([string]$Python)

function Get-DiscoveryApplications {
    param([string]$Name)
    @(Get-Command -Name $Name -CommandType Application -All -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty Path -Unique)
}

function ConvertTo-DiscoveryArgument {
    param([AllowEmptyString()][string]$Value)
    # ProcessStartInfo.ArgumentList is unavailable in Windows PowerShell 5.1.
    # Quote argv using the Windows CRT rules, not shell syntax.
    '"' + [regex]::Replace([regex]::Replace($Value, '(\\*)"', '$1$1\"'), '(\\+)$', '$1$1') + '"'
}

function Invoke-DiscoveryProcess {
    param([string]$Executable, [string[]]$Arguments, [int]$TimeoutMilliseconds = 5000)
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo.FileName = $Executable
    $process.StartInfo.WorkingDirectory = $ExecutionContext.SessionState.Path.CurrentFileSystemLocation.ProviderPath
    $process.StartInfo.Arguments = (($Arguments | ForEach-Object { ConvertTo-DiscoveryArgument $_ }) -join ' ')
    $process.StartInfo.UseShellExecute = $false
    $process.StartInfo.CreateNoWindow = $true
    $process.StartInfo.RedirectStandardOutput = $true
    $process.StartInfo.RedirectStandardError = $true
    $process.StartInfo.StandardOutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $process.StartInfo.StandardErrorEncoding = New-Object System.Text.UTF8Encoding($false)
    # Disable launcher opt-in installation even if inherited from the caller.
    $process.StartInfo.EnvironmentVariables.Remove('PYLAUNCHER_ALLOW_INSTALL')
    $process.StartInfo.EnvironmentVariables.Remove('PYLAUNCHER_ALWAYS_INSTALL')
    $process.StartInfo.EnvironmentVariables['PYTHON_MANAGER_AUTOMATIC_INSTALL'] = 'false'
    try {
        $null = $process.Start()
        $stdout = $process.StandardOutput.ReadToEndAsync()
        $stderr = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutMilliseconds)) {
            try { $process.Kill(); $null = $process.WaitForExit(250) } catch { }
            return [pscustomobject]@{ ExitCode = -1; Stdout = ''; Stderr = "Timed out after $TimeoutMilliseconds milliseconds." }
        }
        # A launcher child can retain the pipe; never wait indefinitely for its EOF.
        if (-not $stdout.Wait(250) -or -not $stderr.Wait(250)) {
            return [pscustomobject]@{ ExitCode = -1; Stdout = ''; Stderr = 'Timed out reading child output.' }
        }
        [pscustomobject]@{ ExitCode = $process.ExitCode; Stdout = $stdout.Result; Stderr = $stderr.Result }
    } catch {
        [pscustomobject]@{ ExitCode = -1; Stdout = ''; Stderr = $_.Exception.Message }
    } finally {
        $process.Dispose()
    }
}

function Add-DiscoveryDiagnostic {
    param($Context, [string]$Source, [string]$Candidate, [string]$Message)
    $Context.Diagnostics.Add([pscustomobject]@{
        source = $Source; candidate = $Candidate; message = $Message
    })
}

function Test-StorePythonAlias {
    param([string]$Path)
    $Path -match '(?i)[\\/]Microsoft[\\/]WindowsApps[\\/]python(?:3(?:\.\d+)?)?\.exe$'
}

function Invoke-DiscoveryAttempt {
    param($Context, [string]$Executable, [string[]]$Arguments, [string]$Source)
    if ($Context.Attempts -ge 24) {
        Add-DiscoveryDiagnostic $Context $Source $Executable 'Discovery stopped at the 24-process safety limit.'
        return $null
    }
    $Context.Attempts++
    Invoke-DiscoveryProcess -Executable $Executable -Arguments $Arguments
}

function Test-DiscoveryPython {
    param($Context, [string]$Executable, [string[]]$Prefix = @(), [string]$Source)
    if (Test-StorePythonAlias $Executable) {
        Add-DiscoveryDiagnostic $Context $Source $Executable 'Skipped Microsoft Store WindowsApps Python alias without launching it.'
        return $null
    }
    if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) {
        Add-DiscoveryDiagnostic $Context $Source $Executable 'Executable path does not exist.'
        return $null
    }
    $probe = 'import encodings,json,pathlib,sys; print(json.dumps({"executable":str(pathlib.Path(sys.executable).resolve()),"version":".".join(map(str,sys.version_info[:3]))}))'
    # Match the execution mode used by helper commands, including the host's
    # actual environment. An isolated-only success must not hide broken stdlib
    # configuration in normal helper execution.
    $result = Invoke-DiscoveryAttempt $Context $Executable (@($Prefix) + @('-c', $probe)) $Source
    if ($null -eq $result) { return $null }
    if ($result.ExitCode -ne 0) {
        $detail = ([string]$result.Stderr).Trim()
        if ($detail.Length -gt 400) { $detail = $detail.Substring(0, 400) }
        Add-DiscoveryDiagnostic $Context $Source $Executable "Import/version probe failed: $detail"
        return $null
    }
    try {
        $info = $result.Stdout | ConvertFrom-Json -ErrorAction Stop
        $version = [version]$info.version
        if ($version -lt [version]'3.12') {
            Add-DiscoveryDiagnostic $Context $Source $Executable "Python $version is below required 3.12."
            return $null
        }
        $resolved = [string]$info.executable
        if (-not [IO.Path]::IsPathRooted($resolved) -or -not (Test-Path -LiteralPath $resolved -PathType Leaf)) {
            throw 'Probe did not return an existing absolute executable path.'
        }
        if (Test-StorePythonAlias $resolved) { throw 'Probe resolved to a Microsoft Store alias.' }
    } catch {
        Add-DiscoveryDiagnostic $Context $Source $Executable "Invalid probe result: $($_.Exception.Message)"
        return $null
    }
    # A launcher or wrapper is not the helper executable. Verify its reported
    # sys.executable directly, and require that direct probe to identify itself.
    if ($Prefix.Count -gt 0 -or -not [string]::Equals([IO.Path]::GetFullPath($Executable), $resolved, [StringComparison]::OrdinalIgnoreCase)) {
        $direct = Invoke-DiscoveryAttempt $Context $resolved @('-c', $probe) $Source
        if ($null -eq $direct) { return $null }
        try {
            if ($direct.ExitCode -ne 0) { throw "Direct executable probe failed: $($direct.Stderr)" }
            $verified = $direct.Stdout | ConvertFrom-Json -ErrorAction Stop
            if ([version]$verified.version -lt [version]'3.12') { throw 'Direct executable is below Python 3.12.' }
            if (-not [string]::Equals([string]$verified.executable, $resolved, [StringComparison]::OrdinalIgnoreCase)) {
                throw 'Direct executable does not identify itself as the resolved executable.'
            }
            $version = [version]$verified.version
        } catch {
            Add-DiscoveryDiagnostic $Context $Source $resolved $_.Exception.Message
            return $null
        }
    }
    Add-DiscoveryDiagnostic $Context $Source $resolved 'Verified imports encodings, json, pathlib and Python >=3.12 in helper execution mode.'
    [pscustomobject]@{ status = 'FOUND'; executable = $resolved; version = $version.ToString(); source = $Source; diagnostics = @($Context.Diagnostics.ToArray()) }
}

function Find-DiscoveryPython {
    param([string]$Python)
    $context = [pscustomobject]@{ Attempts = 0; Diagnostics = New-Object 'System.Collections.Generic.List[object]' }
    if ($Python) {
        try {
            $candidate = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Python)
            $found = Test-DiscoveryPython -Context $context -Executable $candidate -Source 'explicit'
            if ($null -ne $found) { return $found }
        } catch {
            Add-DiscoveryDiagnostic $context 'explicit' $Python $_.Exception.Message
        }
    }
    foreach ($name in @('python', 'python3')) {
        $applications = @(Get-DiscoveryApplications $name | Select-Object -First 24)
        if ($applications.Count -eq 0) { Add-DiscoveryDiagnostic $context "PATH $name" '' 'No installed application found on PATH.' }
        foreach ($candidate in $applications) {
            $found = Test-DiscoveryPython -Context $context -Executable $candidate -Source "PATH $name"
            if ($null -ne $found) { return $found }
        }
    }
    $project = Split-Path -Parent $PSScriptRoot
    foreach ($relative in @('.venv/Scripts/python.exe', '.venv/bin/python')) {
        $candidate = Join-Path $project $relative
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $found = Test-DiscoveryPython -Context $context -Executable $candidate -Source 'project .venv'
            if ($null -ne $found) { return $found }
        }
    }
    foreach ($launcher in @(Get-DiscoveryApplications 'py' | Select-Object -First 24)) {
        $found = Test-DiscoveryPython -Context $context -Executable $launcher -Prefix @('-3.12') -Source 'py -3.12'
        if ($null -ne $found) { return $found }
        $listing = Invoke-DiscoveryAttempt $context $launcher @('-0p') 'py installed versions'
        if ($null -eq $listing -or $listing.ExitCode -ne 0) {
            Add-DiscoveryDiagnostic $context 'py installed versions' $launcher 'Could not enumerate installed launcher versions.'
            continue
        }
        $versions = @(
            foreach ($line in ($listing.Stdout -split "`r?`n")) {
                if ($line -match '^\s*(?<selector>-(?:V:)?(?<major>\d+)\.(?<minor>\d+)[^\s]*)\s+') {
                    $version = [version]("{0}.{1}" -f $Matches.major, $Matches.minor)
                    if ($version -ge [version]'3.12') {
                        [pscustomobject]@{ Version = $version; Selector = $Matches.selector }
                    }
                }
            }
        )
        foreach ($entry in @($versions | Sort-Object -Property @{Expression = 'Version'; Descending = $true}, Selector | Select-Object -First 24)) {
            if ($entry.Selector -eq '-3.12') { continue }
            $found = Test-DiscoveryPython -Context $context -Executable $launcher -Prefix @($entry.Selector) -Source "py $($entry.Selector)"
            if ($null -ne $found) { return $found }
        }
    }
    foreach ($uv in @(Get-DiscoveryApplications 'uv' | Select-Object -First 24)) {
        $result = Invoke-DiscoveryAttempt $context $uv @('python', 'find', '--no-project', '--no-config', '--no-python-downloads', '--offline', '>=3.12') 'uv python find'
        if ($null -eq $result) { continue }
        if ($result.ExitCode -ne 0) {
            Add-DiscoveryDiagnostic $context 'uv python find' $uv "No installed interpreter found: $($result.Stderr)"
            continue
        }
        $candidate = ([string]$result.Stdout).Trim()
        $found = Test-DiscoveryPython -Context $context -Executable $candidate -Source 'uv python find'
        if ($null -ne $found) { return $found }
    }
    [pscustomobject]@{
        status = 'STOP'; executable = $null; version = $null; source = $null
        message = 'STOP: No verified Python >=3.12 with encodings, json and pathlib. Supply -Python with an installed working executable; no installation or download was attempted.'
        diagnostics = @($context.Diagnostics.ToArray())
    }
}

# Dot-sourcing exposes the command/process adapters for isolated, no-install tests.
if ($MyInvocation.InvocationName -ne '.') {
    # Keep stdout to exactly one JSON document; the exit code is not pipeline output.
    $result = Find-DiscoveryPython -Python $Python
    $json = $result | ConvertTo-Json -Depth 5 -Compress
    # ASCII JSON survives Windows PowerShell 5.1's native redirected encoding,
    # while ConvertFrom-Json restores exact Unicode executable paths.
    [regex]::Replace($json, '[^\x00-\x7f]', [System.Text.RegularExpressions.MatchEvaluator]{
        param($match)
        '\u{0:x4}' -f [int][char]$match.Value
    })
    if ($result.status -eq 'FOUND') { exit 0 }
    exit 1
}
