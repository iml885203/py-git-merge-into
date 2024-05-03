# utils.sh

function info_echo() {
  local cyan='\033[0;36m'
  local nc='\033[0m'
  local message=$1
  echo -e "${cyan}[Info] ${message}${nc}"
}

function error_echo() {
  local red='\033[0;31m'
  local nc='\033[0m'
  local message=$1
  echo -e "${red}[Error] ${message}${nc}"
}

function success_echo() {
  local green='\033[0;32m'
  local nc='\033[0m'
  local message=$1
  echo -e "${green}[Success] ${message}${nc}"
}

function warning_echo() {
  local yellow='\033[1;33m'
  local nc='\033[0m'
  local message=$1
  echo -e "${yellow}[Warning] ${message}${nc}"
}

function pull_branch() {
  if ! git diff --quiet; then
    error_echo "There are uncommitted changes in the current branch."
    exit
  fi

  local current_branch=$(git symbolic-ref --short HEAD)
  local target_branch=$1

  git fetch origin $target_branch
  if [ $? -ne 0 ]; then
    error_echo "git fetch failed for branch '${target_branch}'."
    exit
  fi

  git checkout $target_branch > /dev/null 2>&1
  git reset --hard origin/$target_branch
  if [ $? -ne 0 ]; then
    git checkout $current_branch
    error_echo "git pull failed for branch '${target_branch}'."
    exit
  fi
  git checkout $current_branch > /dev/null 2>&1
}

function merge_branch() {
  local current_branch=$(git symbolic-ref --short HEAD)
  local target_branch=$1
  git checkout $target_branch > /dev/null 2>&1
  local merge_output=$(git merge $current_branch) ret="$?"
  local merge_status=$ret
  if [ $merge_status -ne 0 ]; then
    warning_echo "$merge_output"
    git merge --abort
    git checkout $current_branch > /dev/null 2>&1
    if [[ $merge_output == *"CONFLICT"* ]]; then
      error_echo "Merge conflict detected for branch '${target_branch}'."
    else
      error_echo "Merge failed for branch '${target_branch}'."
    fi
    exit
  fi
  echo -e "$merge_output"
  git checkout $current_branch > /dev/null 2>&1
}

function push_branch() {
  local target_branch=$1
  git push origin $target_branch
  if [ $? -ne 0 ]; then
    error_echo "git push failed for branch '${target_branch}'."
    exit
  fi
}