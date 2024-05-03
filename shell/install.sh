#!/bin/bash

_SCRIPT_DIR="$(dirname "$(readlink -f "$0")")/src"

# Check if ~/.zshrc exists
if [ -f "$HOME/.zshrc" ]; then
  # Check if ~/.zshrc contains '# git helper'
  if ! grep -q '# git helper' "$HOME/.zshrc"; then
    echo "" >> "$HOME/.zshrc"
    echo "# git helper" >> "$HOME/.zshrc"

    echo "alias gmi='bash ${_SCRIPT_DIR}/git-merge.sh'" >> "$HOME/.zshrc"
    echo "alias gmip='bash ${_SCRIPT_DIR}/git-merge-push.sh'" >> "$HOME/.zshrc"

    echo "# git helper end" >> "$HOME/.zshrc"
    echo "Git helper aliases added to ~/.zshrc"
  else
    echo "Git helper aliases already exist in ~/.zshrc"
  fi
elif [ -f "$HOME/.bashrc" ]; then
  # Check if ~/.bashrc contains '# git helper'
  if ! grep -q '# git helper' "$HOME/.bashrc"; then
    echo "" >> "$HOME/.bashrc"
    echo "# git helper" >> "$HOME/.bashrc"

    echo "alias gmi='bash ${_SCRIPT_DIR}/git-merge.sh'" >> "$HOME/.bashrc"
    echo "alias gmip='bash ${_SCRIPT_DIR}/git-merge-push.sh'" >> "$HOME/.bashrc"

    echo "# git helper end" >> "$HOME/.bashrc"
    echo "Git helper aliases added to ~/.bashrc"
  else
    echo "Git helper aliases already exist in ~/.bashrc"
  fi
else
  echo "Neither ~/.zshrc nor ~/.bashrc found, unable to add Git helper aliases"
fi