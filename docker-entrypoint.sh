#!/bin/sh
python configure.py
service haproxy start
python server.py
