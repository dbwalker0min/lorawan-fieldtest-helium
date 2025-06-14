param(
    [int]$UseOverride = 0
)

# Normalize input
$UseOverride = $UseOverride -ne 0

Write-Host "Port Exposure Script Started. UseOverride: $UseOverride"

# Configuration
$serviceName = "db"
$baseCompose = "docker-compose.yml"
$overrideCompose = "scripts\open_db_port5432.yaml"
$targetPort = "5432"  # Change to the port you're monitoring

# Helper function to get the published port
function Get-ServicePublishedPorts {
    $containerId = docker-compose -f $baseCompose ps -q $serviceName
    if (-not $containerId) {
        return @()
    }

    $portBindings = docker inspect -f '{{json .NetworkSettings.Ports }}' $containerId 2>$null | ConvertFrom-Json
    if ($portBindings -eq $null) {
        return @()
    }

    return $portBindings.PSObject.Properties | Where-Object {
        $_.Value -ne $null
    } | ForEach-Object {
        $_.Name.Split("/")[0]
    }
}

# Determine current exposure
$currentlyExposedPorts = Get-ServicePublishedPorts
WRite-Host "Currently exposed ports for service '$serviceName': $($currentlyExposedPorts -join ', ')"
$portExposed = $currentlyExposedPorts -contains $targetPort

# Decide if action is necessary
if ($UseOverride -and $portExposed) {
    Write-Host "Port is already exposed. No action needed."
    return
}

if (-not $UseOverride -and -not $portExposed) {
    Write-Host "Port is already unexposed. No action needed."
    return
}

# Otherwise, change is needed
Write-Host "Port exposure state needs to change. Restarting service: $serviceName..."

# Stop and remove the service's container
$containerId = docker-compose -f $baseCompose ps -q $serviceName
if ($containerId) {
    docker-compose -f $baseCompose stop $serviceName
    docker-compose -f $baseCompose rm -f $serviceName
}

# Rebuild/start service with or without override
if ($UseOverride) {
    Write-Host "Starting service with port exposed (override)..."
    docker-compose -f $baseCompose -f $overrideCompose up -d --build $serviceName
} else {
    Write-Host "Starting service without port exposed..."
    docker-compose -f $baseCompose up -d --build $serviceName
}
