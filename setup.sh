#!/bin/bash

# Download Python 3 and depencies needed for test
sudo apt update
sudo apt install python3
sudo python3 -m pip install pyyaml

# Install tix-time-client
git clone https://github.com/TiX-measurements/tix-time-client.git