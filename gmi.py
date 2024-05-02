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

@click.command()
@click.argument('target_branch')
def gmi(target_branch):
#     check()
    pull(target_branch)

if __name__ == '__main__':
    gmi()
