# hello.py

import click
import subprocess

def check():
    if subprocess.call(['git', 'diff', '--quiet']) != 0:
        click.echo(click.style("[Error] There are uncommitted changes in the current branch.", fg='red'))
        raise click.Abort()

def pull(target_branch):
    current_branch = subprocess.check_output(['git', 'symbolic-ref', '--short', 'HEAD'], text=True).strip()

    click.echo(click.style(f"[Info] Pulling changes from '{target_branch}' branch...", fg='cyan'))

    fetch_process = subprocess.run(['git', 'fetch', 'origin', target_branch])
    if fetch_process.returncode != 0:
        click.echo(click.style(f"[Error] git fetch failed for branch '{target_branch}'.", fg='red'))
        raise click.Abort()

    subprocess.run(['git', 'checkout', target_branch], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    reset_process = subprocess.run(['git', 'reset', '--hard', f'origin/{target_branch}'])
    if reset_process.returncode != 0:
        click.echo(click.style(f"[Error] git reset failed for branch '{target_branch}'.", fg='red'))
        subprocess.run(['git', 'checkout', current_branch], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        raise click.Abort()

    subprocess.run(['git', 'checkout', current_branch], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# Bash script
# function merge_branch() {
#   local current_branch=$(git symbolic-ref --short HEAD)
#   local target_branch=$1
#   git checkout $target_branch > /dev/null 2>&1
#   local merge_output=$(git merge $current_branch) ret="$?"
#   local merge_status=$ret
#   if [ $merge_status -ne 0 ]; then
#     warning_echo "$merge_output"
#     git merge --abort
#     git checkout $current_branch > /dev/null 2>&1
#     if [[ $merge_output == *"CONFLICT"* ]]; then
#       error_echo "Merge conflict detected for branch '${target_branch}'."
#     else
#       error_echo "Merge failed for branch '${target_branch}'."
#     fi
#     exit
#   fi
#   echo -e "$merge_output"
#   git checkout $current_branch > /dev/null 2>&1
# }
def merge(target_branch):
    current_branch = subprocess.check_output(['git', 'symbolic-ref', '--short', 'HEAD'], text=True).strip()

    click.echo(click.style(f"[Info] Merging changes from '{current_branch}' to '{target_branch}' branch...", fg='cyan'))

    # 切换到目标分支
    subprocess.run(['git', 'checkout', target_branch], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # 执行合并操作
    merge_process = subprocess.run(['git', 'merge', current_branch], capture_output=True, text=True)
    merge_status = merge_process.returncode
    if merge_status != 0:
        click.echo(click.style(merge_process.stdout, fg='yellow'))
        subprocess.run(['git', 'merge', '--abort'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(['git', 'checkout', current_branch], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if "CONFLICT" in merge_process.stdout:
            click.echo(click.style(f"[Error] Merge conflict detected for branch '{target_branch}'.", fg='red'))
        else:
            click.echo(click.style(f"[Error] Merge failed for branch '{target_branch}'.", fg='red'))
        raise click.Abort()

    # 输出合并结果
    click.echo(click.style(merge_process.stdout))

    # 切换回当前分支
    subprocess.run(['git', 'checkout', current_branch], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


@click.command()
@click.argument('target_branch')
def gmi(target_branch):
#     check()
    pull(target_branch)
    merge(target_branch)
    click.echo(click.style(f"[Success] Merged changes from current branch to '{target_branch}' branch.", fg='green'))

if __name__ == '__main__':
    gmi()
