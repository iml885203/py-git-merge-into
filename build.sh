#!/bin/bash

pyinstaller --onefile gmip.py gmi.py
cp dist/gmip dist/gmi bin