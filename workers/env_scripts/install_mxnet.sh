#!/usr/bin/env bash
read -p 'Home directory: ' directory

cd $directory
git clone https://github.com/apache/incubator-mxnet.git
pip install mxnet-mkl==1.5.1 --user
mkdir -p /tmp/mxnet_job
cp incubator-mxnet/example/gluon/*.py /tmp/mxnet_job