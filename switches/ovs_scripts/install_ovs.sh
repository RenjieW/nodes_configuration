#!/usr/bin/env bash

apt install -y openvswitch-switch
apt purge -y openvswitch-common
apt install -y openvswitch-switch