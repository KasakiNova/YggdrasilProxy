#!/usr/bin/bash

# 设定变量
version="snapshots"
platform=$(uname -p)
outputFileName="YggdrasilProxy-${platform}-${version}"
outputPath="build"
sourceFile="main.py"
systemThread=$(nproc)
pypiLink="https://pypi.python.org/simple"
# pypiLink="https://pypi.mirrors.ustc.edu.cn/simple/"

rm -rf ./${outputPath}
mkdir -p ${outputPath}

# Python虚拟环境
if [ ! -d "./buildVenv" ];then
  /usr/bin/python3 -m venv ./buildVenv
fi

source ./buildVenv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt -i ${pypiLink}
pip install nuitka -i ${pypiLink}

time python3 -m nuitka \
  --follow-imports --standalone --onefile \
  --show-memory --show-progress \
  --include-package=requests --jobs="${systemThread}" \
  --output-dir=${outputPath} --output-filename="${outputFileName}" \
  ${sourceFile}

# 退出虚拟环境
deactivate
