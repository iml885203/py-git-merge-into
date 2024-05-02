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

def merge(target_branch):
    current_branch = subprocess.check_output(['git', 'symbolic-ref', '--short', 'HEAD'], text=True).strip()

    click.echo(click.style(f"[Info] Merging changes from '{current_branch}' to '{target_branch}' branch...", fg='cyan'))

    subprocess.run(['git', 'checkout', target_branch], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

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

    click.echo(click.style(merge_process.stdout))

    subprocess.run(['git', 'checkout', current_branch], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def push(target_branch):
    click.echo(click.style(f"[Info] Pushing changes to '{target_branch}' branch...", fg='cyan'))

    push_process = subprocess.run(['git', 'push', 'origin', target_branch])
    push_status = push_process.returncode

    if push_status != 0:
        click.echo(click.style(f"[Error] git push failed for branch '{target_branch}'.", fg='red'))
        raise click.Abort()

    click.echo(click.style(f"[Success] Pushed changes to '{target_branch}' branch.", fg='green'))

@click.command()
@click.argument('target_branch')
def gmip(target_branch):
    check()
    pull(target_branch)
    merge(target_branch)
    click.echo(click.style(f"[Success] Merged changes from current branch to '{target_branch}' branch.", fg='green'))

if __name__ == '__main__':
    gmip()
