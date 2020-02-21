#!/usr/bin/env bash

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# build and install are separated so changes to build don't invalidate
# the whole docker cache for the image

set -ex
apt-get update || true

/usr/testbed/bin/mkextrafs /mnt
chmod 777 /mnt

# Avoid interactive package installers such as tzdata.
export DEBIAN_FRONTEND=noninteractive

apt-get install -y \
    apt-transport-https \
    build-essential \
    ca-certificates \
    curl \
    git \
    libatlas-base-dev \
    libcurl4-openssl-dev \
    libjemalloc-dev \
    libhdf5-dev \
    liblapack-dev \
    libopenblas-dev \
    libopencv-dev \
    libturbojpeg \
    libzmq3-dev \
    ninja-build \
    software-properties-common \
    sudo \
    unzip \
    vim-nox \
    wget

# Use libturbojpeg package as it is correctly compiled with -fPIC flag
# https://github.com/HaxeFoundation/hashlink/issues/147 
ln -s /usr/lib/x86_64-linux-gnu/libturbojpeg.so.0.1.0 /usr/lib/x86_64-linux-gnu/libturbojpeg.so


# Note: we specify an exact cmake version to work around a cmake 3.10 CUDA 10 issue.
# Reference: https://github.com/clab/dynet/issues/1457
mkdir /usr/bin/cmake && cd /usr/bin/cmake
wget -nv https://cmake.org/files/v3.13/cmake-3.13.0-Linux-x86_64.sh
sh cmake-3.13.0-Linux-x86_64.sh --prefix=/usr/bin/cmake --skip-license
ln -s /usr/bin/cmake/bin/cmake /usr/local/bin/cmake
rm cmake-3.13.0-Linux-x86_64.sh
cmake --version
