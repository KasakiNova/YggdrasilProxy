#!/usr/bin/bash

# 设定变量
outputFileName="AndreaYggdrasilProxy"
outputPath="./build"
sourceFile="launcher.py"
systemThread=$(nproc)
pypiLink="https://pypi.mirrors.ustc.edu.cn/simple"
# 判断输出目录是否存在
if [ -d "${outputPath}" ];then
    echo -e "Folder already exists \nDelete Folder"
    rm -rf ${outputPath}
else
    echo -e "Folder does not exist \nCreate Folder"
fi
mkdir -p ${outputPath}

# Python虚拟环境
if [ -d "./venv" ];then
    rm -rf ./venv
fi
/usr/bin/python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt -i ${pypiLink}
pip install nuitka -i ${pypiLink}

time python3 -m nuitka --follow-imports --standalone --onefile --show-memory  --show-progress --include-package=requests --jobs=${systemThread} --output-dir=${outputPath} --output-filename=${outputFileName} ${sourceFile}

# 退出虚拟环境
deactivate
