import click
from utils import check_branches_not_same, check_for_uncommitted_changes, git_checkout, git_fetch, git_reset_hard, git_merge, git_push

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('target_branch')
def gmip(target_branch):
    """Merge current branch to target branch and push."""
    try:
        check_branches_not_same(target_branch)
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
        click.echo(click.style(f"[Error] {str(e)}", fg='red'))


if __name__ == '__main__':
    gmip()
