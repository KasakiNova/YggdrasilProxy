$version="snapshots"
$outputFileName="YggdrasilProxy-${version}"
$outputPath="build"
$sourceFile="main.py"
$systemThread=$(Get-WmiObject Win32_ComputerSystem | Select-Object -ExpandProperty NumberOfLogicalProcessors)
$pypiLink="https://pypi.python.org/simple"
#$pypiLink="https://pypi.mirrors.ustc.edu.cn/simple"

Remove-Item -Recurse -Path $outputPath -Force
New-Item -ItemType Directory -Path $outputPath

Write-Output "Create Python Venv"
if (Test-Path -Path buildVenv -PathType Container) {}
else {python.exe -m venv buildVenv}

Write-Output "Install Packages"
.\buildVenv\Scripts\Activate.ps1
python.exe -m pip install --upgrade pip -i ${pypiLink}
pip install -r requirements.txt -i ${pypiLink}
pip install nuitka -i ${pypiLink}

Write-Output "Build Now"
python -m nuitka --follow-imports --standalone --onefile `
--show-memory  --show-progress `
--include-package=requests `
--jobs=$systemThread --lto=yes `
--output-dir=$outputPath --output-filename=${outputFileName} `
${sourceFile}

Read-Host -Prompt "Press any key to continue"