#!/bin/bash

cd cli
pyinstaller --onefile gmi.py gmip.py
cp dist/gmi bin
cp dist/gmip bin
cd ..