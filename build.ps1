param (
    [string]$version = "snapshots",
    [string]$sourceFile = "main.py"
)

$outputFileName = "YggdrasilProxy-${version}"
$outputPath = "build"
$systemThread = (Get-WmiObject Win32_ComputerSystem | Select-Object -ExpandProperty NumberOfLogicalProcessors)
$pypiLink = "https://pypi.python.org/simple"
#$pypiLink="https://pypi.mirrors.ustc.edu.cn/simple"

function New-VirtualEnvironment {
    Write-Output "Creating Python virtual environment..."
    if (-Not (Test-Path -Path buildVenv -PathType Container)) {
        python.exe -m venv .venv
    }
}

function Install-Packages {
    Write-Output "Installing packages..."
    .\.venv\Scripts\Activate.ps1
    python.exe -m pip install --upgrade pip -i ${pypiLink}
    pip install --no-cache-dir -r requirements.txt -i ${pypiLink}
    pip install --no-cache-dir nuitka -i ${pypiLink}
}

function Invoke-ProjectBuild {
    Write-Output "Building project now..."
    python -OO -m nuitka `
        --clang `
        --follow-imports `
        --standalone `
        --onefile `
        --show-memory `
        --show-progress `
        --include-package=requests `
        --jobs=$systemThread `
        --lto=yes `
        --python-flag=-OO `
        --output-dir=$outputPath `
        --output-filename=${outputFileName} `
        ${sourceFile}
}

# Main script execution
Remove-Item -Recurse -Path $outputPath -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $outputPath

New-VirtualEnvironment
Install-Packages
Invoke-ProjectBuild

if ($LASTEXITCODE -ne 0) {
    Write-Output "Build failed."
    exit $LASTEXITCODE
} else {
    Write-Output "Build succeeded."
}
