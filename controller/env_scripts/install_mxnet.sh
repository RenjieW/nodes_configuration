#!/usr/bin/env bash
pip install mxnet-mkl --user
cd ~
git clone https://github.com/apache/incubator-mxnet.git
sudo mkdir /tmp/mxnet_job
sudo cp ~/incubator-mxnet/example/gluon/image_classification.py /tmp/mxnet_job/
sudo cp ~/incubator-mxnet/example/gluon/data.py /tmp/mxnet_job/