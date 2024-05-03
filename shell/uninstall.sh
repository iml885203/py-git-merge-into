#!/bin/bash

# Check if Git helper aliases exist in ~/.zshrc
if [ -f "$HOME/.zshrc" ] && grep -q '# git helper' "$HOME/.zshrc"; then
  # Remove Git helper aliases from ~/.zshrc
  sed -i '' '/# git helper/,/# git helper end/d' "$HOME/.zshrc"
  echo "Git helper aliases removed from ~/.zshrc"
fi

# Check if Git helper aliases exist in ~/.bashrc
if [ -f "$HOME/.bashrc" ] && grep -q '# git helper' "$HOME/.bashrc"; then
  # Remove Git helper aliases from ~/.bashrc
  sed -i '' '/# git helper/,/# git helper end/d' "$HOME/.bashrc"
  echo "Git helper aliases removed from ~/.bashrc"
fi
