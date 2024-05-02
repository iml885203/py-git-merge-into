# gmip

> Useful command, Colorful result!!!

## Usage
- gmi {branch}: current branch merge into {branch}
- gmip {branch}: current branch merge into {branch} and push

## Installation

```bash
./install.sh
```

## Uninstall

```bash
./uninstall.sh
```

## Development

### Install packages
```bash
pip install -r requirements.txt
```

### Run
```bash
python gmi.py {branch}
python gmip.py {branch}
```

### Build
```bash
pyinstaller --onefile gmip.py gmi.py
```