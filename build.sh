#!/bin/bash

cd cli
pyinstaller --onefile gmi.py gmi.py
cp dist/gmip dist/gmi bin
cd ..