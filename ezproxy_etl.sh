#! /bin/bash

# enter python virtual environment
source venv/bin/activate; 

# run ezproxy_etl for the current day
python ezproxy_etl.py
