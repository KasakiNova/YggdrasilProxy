$outputFileName="YggdrasilProxy"
$outputPath="build"
$sourceFile="main.py"
$systemThread=$(Get-WmiObject Win32_ComputerSystem | Select-Object -ExpandProperty NumberOfLogicalProcessors)
$pypiLink="https://pypi.mirrors.ustc.edu.cn/simple"

if (Test-Path -Path $outputPath -PathType Container) {
    #Remove-Item -Recurse -Path $outputPath -Force
}
else {
    New-Item -ItemType Directory -Path $outputPath
}

Write-Output "Create Python Venv"
python.exe -m venv .venv

Write-Output "Install Packages"
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -i ${pypiLink}
pip install nuitka -i ${pypiLink}

Write-Output "Build Now"
python -m nuitka --follow-imports --standalone --onefile --show-memory  --show-progress --include-package=requests --jobs=${systemThread} --output-dir=${outputPath} --output-filename=${outputFileName} ${sourceFile}
