#!/usr/bin/env bash

echo 'rjwu:1229' | chpasswd
echo '1229' | sudo -u rjwu chsh -s /bin/bash

cd ./ssh_script
./ssh_config.sh

cd ../hosts_script
./change_hosts.sh

cd ../env_script
./ubuntu_python.sh

cd ../ovs_scripts
./install_ovs.sh