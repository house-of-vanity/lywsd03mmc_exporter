#!/bin/bash

# start services
service dbus start
service bluetooth start


python3 ./bt_exporter.py
