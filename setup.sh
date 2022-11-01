#!/bin/sh

echo "Setting up the environment..."
sudo apt update -y
sudo apt install -y python3-pip
pip3 install virtualenv
python3 -m venv PyNFS-ENV
. PyNFS-ENV/bin/activate
pip3 install -r requirements.txt
echo "Done!"