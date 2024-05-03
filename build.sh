#!/bin/bash

pyinstaller --onefile cli/gmip.py cli/gmi.py
cp dist/gmip dist/gmi bin