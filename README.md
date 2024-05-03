# Git Merge Into

> Useful command, Colorful result!!!

## Usage
- gmi {branch}: current branch merge into {branch}
- gmip {branch}: current branch merge into {branch} and push

---

## Installation

### CLI version
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/iml885203/git-merge-into/main/install-cli.sh)"
```

## Uninstall

### CLI version
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/iml885203/git-merge-into/main/uninstall-cli.sh)"
```

## Development CLI

```
git clone git@github.com:iml885203/git-merge-into.git
```

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
./build-cli.sh
```