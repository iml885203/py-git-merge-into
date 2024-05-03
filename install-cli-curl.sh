#!/bin/bash

curl -o /tmp/gmi https://raw.githubusercontent.com/iml885203/git-merge-into/main/cli/bin/gmi
curl -o /tmp/gmip https://raw.githubusercontent.com/iml885203/git-merge-into/main/cli/bin/gmip
sudo mv /tmp/gmi /usr/local/bin/gmi
sudo mv /tmp/gmip /usr/local/bin/gmip
sudo chmod +x /usr/local/bin/gmi
sudo chmod +x /usr/local/bin/gmip

echo "installed successfully!"
