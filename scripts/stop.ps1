# Stops the Task Tracker API (port 8000) and UI (port 5500).
$ErrorActionPreference = "Continue"

function Stop-ServerOnPort {
    param(
        [int]$Port,
        [string]$Name
    )

    $listenerPids = @(
        Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
            Select-Object -ExpandProperty OwningProcess -Unique
    ) | Where-Object { $_ -and $_ -gt 4 }

    if (-not $listenerPids) {
        Write-Host "$Name (port $Port) is not running."
        return
    }

    foreach ($procId in $listenerPids) {
        $targetId = $procId
        $current = Get-CimInstance Win32_Process -Filter "ProcessId=$procId" -ErrorAction SilentlyContinue

        while ($current) {
            $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$($current.ParentProcessId)" -ErrorAction SilentlyContinue
            if (-not $parent) {
                break
            }

            $parentName = $parent.Name
            $parentCommand = [string]$parent.CommandLine
            $isPythonParent = $parentName -match '^(python|py)(\.exe)?$'
            $isStartWindow = $parentName -match '^powershell(\.exe)?$' -and
                $parentCommand -match 'uvicorn app\.main:app|http\.server 5500'

            if ($isPythonParent -or $isStartWindow) {
                $targetId = $parent.ProcessId
                $current = $parent
                continue
            }

            break
        }

        Write-Host "Stopping $Name (PID $targetId) on port $Port..."
        & taskkill.exe /PID $targetId /T /F 2>$null | Out-Null
    }
}

Stop-ServerOnPort -Port 8000 -Name "API"
Stop-ServerOnPort -Port 5500 -Name "UI"
Write-Host "Done."
