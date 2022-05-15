#!/bin/sh
if [ -d "./venv" ]
then
    . venv/bin/activate
else
    echo "No installation found. Installing..."
    python3 -m virtualenv venv
    . venv/bin/activate
    echo "Installing components..."
    pip3 install -r requirements.txt
    echo "Installation finished!"
fi
python3 src/main.pyw
exit 0
