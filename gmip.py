import click
import subprocess

def run_git_command(command, *args):
    """Run a git command with given arguments."""
    return subprocess.run(['git', command] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

def check_for_uncommitted_changes():
    """Check for uncommitted changes."""
    if run_git_command('diff', '--quiet').returncode != 0:
        raise click.ClickException("There are uncommitted changes in the current branch.")

def git_checkout(branch):
    """Checkout the given branch."""
    run_git_command('checkout', branch)

def git_fetch(branch):
    """Fetch the given branch."""
    fetch_process = run_git_command('fetch', 'origin', branch)
    if fetch_process.returncode != 0:
        raise click.ClickException(f"git fetch failed for branch '{branch}'.")

def git_reset_hard(branch):
    """Reset the branch to its remote state."""
    reset_process = run_git_command('reset', '--hard', f'origin/{branch}')
    if reset_process.returncode != 0:
        raise click.ClickException(f"git reset failed for branch '{branch}'.")

    click.echo(click.style(reset_process.stdout))

def git_merge(branch):
    """Merge the given branch into the current branch."""
    merge_process = run_git_command('merge', branch)
    merge_status = merge_process.returncode

    if merge_status != 0:
        click.echo(click.style(merge_process.stderr, fg='yellow'))
        run_git_command('merge', '--abort')
        if "CONFLICT" in merge_process.stderr:
#             click.echo(click.style(f"[Error] Merge conflict detected for branch '{branch}'.", fg='red'))
            raise click.ClickException(f"Merge conflict detected for branch '{branch}'.")
        else:
            raise click.ClickException(f"Merge failed for branch '{branch}'.")
    click.echo(click.style(merge_process.stdout))

def git_push(branch):
    """Push changes to the given branch."""
    push_process = run_git_command('push', 'origin', branch)
    if push_process.returncode != 0:
        raise click.ClickException(f"git push failed for branch '{branch}'.")

@click.command()
@click.argument('target_branch')
def gmip(target_branch):
    """Git Merge, Pull, and Push."""
    try:
        check_for_uncommitted_changes()

        click.echo(click.style(f"[Info] Pulling changes from '{target_branch}' branch...", fg='cyan'))
        git_checkout(target_branch)
        git_fetch(target_branch)
        git_reset_hard(target_branch)
        git_checkout('-')  # Switch back to previous branch

        click.echo(click.style(f"[Info] Merging changes from current branch to '{target_branch}' branch...", fg='cyan'))
        git_checkout(target_branch)
        git_merge('-')
        git_checkout('-')  # Switch back to previous branch

        click.echo(click.style(f"[Info] Pushing changes to '{target_branch}' branch...", fg='cyan'))
        git_push(target_branch)

        click.echo(click.style(f"[Success] Merged changes from current branch to '{target_branch}' branch.", fg='green'))
    except click.ClickException as e:
        click.echo(click.style(str(e), fg='red'))

if __name__ == '__main__':
    gmip()