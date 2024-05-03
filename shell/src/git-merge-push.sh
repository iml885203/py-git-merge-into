# git-merge-push.sh

_SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

source "${_SCRIPT_DIR}/utils.sh"

if [ -z "$1" ]; then
  error_echo "Please provide the target branch name as the first argument."
  exit 1
fi

_CURRENT_BRANCH=$(git symbolic-ref --short HEAD)
_TARGET_BRANCH=$1

info_echo "Pulling changes from '${_TARGET_BRANCH}' branch..."
pull_branch $_TARGET_BRANCH

info_echo "Merging changes from '${_CURRENT_BRANCH}' to '${_TARGET_BRANCH}' branch..."
merge_branch $_TARGET_BRANCH

info_echo "Pushing changes to '${_TARGET_BRANCH}' branch..."
push_branch $_TARGET_BRANCH

success_echo "Merged changes from '${_CURRENT_BRANCH}' to '${_TARGET_BRANCH}' branch."
