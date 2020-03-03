#!/usr/bin/env bash

echo 'rjwu:1229' | chpasswd
echo '1229' | sudo -u rjwu chsh -s /bin/bash

cd ./ssh_script
./ssh_config.sh

cd ../hosts_script
./change_hosts.sh

cd ../env_scripts
./ubuntu_core.sh
./ubuntu_python.sh

read -p 'Package to install: ' Package
if [ "$Package" = "mxnet" ]; then
    sudo -u rjwu ./install_mxnet.sh
else
    ./sketchdlc_env.sh
    sudo -u rjwu ./install_sketchdlc.sh
fi