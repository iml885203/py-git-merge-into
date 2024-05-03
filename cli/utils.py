import click
import subprocess

def run_git_command(command, *args):
    """Run a git command with given arguments."""
    return subprocess.run(['git', command] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

def check_branches_not_same(target_branch):
    """Check if the current branch is not the same as the target branch."""
    current_branch = run_git_command('rev-parse', '--abbrev-ref', 'HEAD').stdout.strip()
    if current_branch == target_branch:
        raise click.ClickException(f"Cannot merge the '{current_branch}' into '{target_branch}' branch.")

def check_for_uncommitted_changes():
    """Check for uncommitted changes."""
    if run_git_command('diff', '--quiet').returncode != 0:
        raise click.ClickException("There are uncommitted changes in the current branch.")

def get_current_branch():
    """Get the current branch."""
    return run_git_command('rev-parse', '--abbrev-ref', 'HEAD').stdout.strip()

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

    click.echo(reset_process.stdout)

def git_merge(branch):
    """Merge the given branch into the current branch."""
    merge_process = run_git_command('merge', branch)
    merge_status = merge_process.returncode

    if merge_status != 0:
        click.echo(click.style(merge_process.stderr, fg='yellow'))
        run_git_command('merge', '--abort')
        if "CONFLICT" in merge_process.stdout:
            raise click.ClickException(f"Merge conflict detected for branch '{branch}'.")
        else:
            raise click.ClickException(f"Merge failed for branch '{branch}'.")
    click.echo(merge_process.stdout)

def git_push(branch):
    """Push changes to the given branch."""
    push_process = run_git_command('push', 'origin', branch)
    if push_process.returncode != 0:
        raise click.ClickException(f"git push failed for branch '{branch}'.")
    click.echo(push_process.stderr) # git push output goes into stderr
