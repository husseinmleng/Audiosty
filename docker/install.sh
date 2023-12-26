#!/bin/sh

pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
pip install --no-cache-dir gunicorn
pip install --no-cache-dir -r requirements.txt
mkdir app