#
# Claude Statusline - Setup Script (Windows PowerShell)
# Installs the package and runs first-time initialization
#
# Usage: powershell -ExecutionPolicy Bypass -File setup_windows.ps1
#

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Claude Statusline - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Check Python ---
$python = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 8) {
                $python = $cmd
                break
            }
        }
    } catch {}
}

if (-not $python) {
    Write-Host "[!] Python 3.8+ is required but not found." -ForegroundColor Red
    Write-Host "    Download from https://python.org"
    exit 1
}

$pyVersion = & $python --version 2>&1
Write-Host "[+] $pyVersion" -ForegroundColor Green

# --- Check pip ---
try {
    $pipVer = & $python -m pip --version 2>&1
    Write-Host "[+] pip found" -ForegroundColor Green
} catch {
    Write-Host "[!] pip is not installed." -ForegroundColor Red
    Write-Host "    Run: $python -m ensurepip --upgrade"
    exit 1
}

# --- Install or upgrade ---
Write-Host ""
Write-Host "Installing claude-statusline..." -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (Test-Path "$scriptDir\pyproject.toml") {
    # Installing from source
    Write-Host "[i] Installing from source..." -ForegroundColor Yellow
    & $python -m pip install -e $scriptDir --quiet 2>&1 | Out-Null
} else {
    # Installing from PyPI
    Write-Host "[i] Installing from PyPI..." -ForegroundColor Yellow
    & $python -m pip install --upgrade claude-statusline --quiet 2>&1 | Out-Null
}

Write-Host "[+] Package installed" -ForegroundColor Green

# --- Verify installation ---
try {
    $version = & $python -m claude_statusline.cli --version 2>&1
    Write-Host "[+] $version" -ForegroundColor Green
} catch {
    Write-Host "[!] Installation verification failed" -ForegroundColor Red
    exit 1
}

# --- Check and fix PATH ---
Write-Host ""
Write-Host "Checking PATH..." -ForegroundColor Cyan

# Find scripts directories
$siteScripts = & $python -c "import sysconfig; print(sysconfig.get_path('scripts'))" 2>$null
$userScripts = & $python -c "import site; print(site.getusersitepackages().replace('site-packages','Scripts'))" 2>$null

$pathDirs = $env:Path -split ";"
$needsPathUpdate = $true

foreach ($dir in @($siteScripts, $userScripts)) {
    if ($dir -and ($pathDirs -contains $dir)) {
        $needsPathUpdate = $false
        break
    }
}

if ($needsPathUpdate) {
    # Find which scripts dir actually has claude-statusline.exe
    $targetDir = $null
    foreach ($dir in @($siteScripts, $userScripts)) {
        if ($dir -and (Test-Path "$dir\claude-statusline.exe")) {
            $targetDir = $dir
            break
        }
    }

    if (-not $targetDir) {
        # Check common locations
        $pyMajor = & $python -c "import sys; print(sys.version_info.major)" 2>$null
        $pyMinor = & $python -c "import sys; print(sys.version_info.minor)" 2>$null
        $roamingScripts = "$env:APPDATA\Python\Python$pyMajor$pyMinor\Scripts"
        if (Test-Path "$roamingScripts\claude-statusline.exe") {
            $targetDir = $roamingScripts
        }
    }

    if ($targetDir) {
        Write-Host "[!] Scripts directory not in PATH: $targetDir" -ForegroundColor Yellow
        Write-Host ""

        $choice = Read-Host "    Add to user PATH? [Y/n]"
        if ($choice -eq "" -or $choice -eq "Y" -or $choice -eq "y") {
            $currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
            if ($currentUserPath -notlike "*$targetDir*") {
                [Environment]::SetEnvironmentVariable("Path", "$currentUserPath;$targetDir", "User")
                $env:Path = "$env:Path;$targetDir"
                Write-Host "    [+] Added to user PATH" -ForegroundColor Green
                Write-Host "    [i] New terminals will have this automatically" -ForegroundColor Yellow
            } else {
                Write-Host "    [=] Already in user PATH (current session may need refresh)" -ForegroundColor Yellow
                $env:Path = "$env:Path;$targetDir"
            }
        }
    }
}
else {
    Write-Host "[+] Scripts directory already in PATH" -ForegroundColor Green
}

# --- Run init ---
Write-Host ""
Write-Host "Running first-time setup..." -ForegroundColor Cyan
Write-Host ""
& $python -m claude_statusline.cli init

# --- Start daemon ---
Write-Host "Starting daemon..." -ForegroundColor Cyan
try {
    Start-Process -FilePath $python -ArgumentList "-m", "claude_statusline.daemon", "--start" -WindowStyle Hidden -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "[+] Daemon started" -ForegroundColor Green
} catch {
    Write-Host "[!] Could not auto-start daemon (start manually: claude-statusline daemon --start)" -ForegroundColor Yellow
}

# --- Final ---
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  claude-statusline status   - Show session status" -ForegroundColor Green
Write-Host "  claude-statusline theme    - Browse 100 themes" -ForegroundColor Green
Write-Host "  claude-statusline --help   - All commands" -ForegroundColor Green
Write-Host ""

# Show status preview
Write-Host "Status preview:" -ForegroundColor Cyan
try {
    & $python -m claude_statusline.cli status 2>$null
} catch {
    Write-Host "(Status will be available after Claude Code generates data)"
}
Write-Host ""
