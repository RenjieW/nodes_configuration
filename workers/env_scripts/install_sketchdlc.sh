#!/usr/bin/env bash
cd /users/rjwu
git clone https://github.com/RenjieW/SketchDLC.git

cd /users/rjwu/SketchDLC
mkdir build && cd build
cmake -DUSE_CUDA=0 -DCMAKE_BUILD_TYPE=Release -GNinja ..
ninja -v
cd ../python
pip install --user -e .

echo "export KMP_DUPLICATE_LIB_OK=TRUE" >> /users/rjwu/.profile
source /users/rjwu/.profile

mkdir /mnt/data_trace