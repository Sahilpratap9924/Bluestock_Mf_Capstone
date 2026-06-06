<#
.SYNOPSIS
Register a Windows scheduled task to run the Bluestock ETL pipeline every weekday at 8 PM.

.DESCRIPTION
This script creates or replaces a scheduled task named BluestockMF_ETL.
It runs `python scripts/auto_etl.py` with the requested mfapi.in URL and output path.
#>

param(
    [string]$TaskName = 'BluestockMF_ETL',
    [string]$PythonExe,
    [string]$ProjectRoot,
    [string]$MfapiUrl,
    [string]$OutputCsv,
    [switch]$Force
)

if (-not $ProjectRoot) {
    $ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
}

if (-not $PythonExe) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        Write-Error 'Python executable not found in PATH. Provide -PythonExe explicitly.'
        exit 1
    }
    $PythonExe = $pythonCmd.Source
}

if (-not $MfapiUrl) {
    Write-Error 'Please provide a mfapi.in URL with -MfapiUrl, for example https://api.mfapi.in/mf/<scheme-code>'
    exit 1
}

if (-not $OutputCsv) {
    $OutputCsv = Join-Path $ProjectRoot 'data\raw\latest_navs.csv'
}

$AutoEtlScript = Join-Path $ProjectRoot 'scripts\auto_etl.py'
$Argument = "`"$AutoEtlScript`" --url `"$MfapiUrl`" --out `"$OutputCsv`""
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument $Argument
$Trigger = New-ScheduledTaskTrigger -Weekly -Days Monday,Tuesday,Wednesday,Thursday,Friday -At 20:00
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    if ($Force) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    } else {
        Write-Output "Task '$TaskName' already exists. Use -Force to recreate it."
        exit 0
    }
}

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description 'Run Bluestock ETL every weekday at 8 PM with live NAV fetch from mfapi.in.'

Write-Output "Scheduled task '$TaskName' registered for weekdays at 20:00."