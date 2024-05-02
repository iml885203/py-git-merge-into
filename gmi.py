# hello.py

import click

@click.command()
@click.argument('target_branch')
def gmi(target_branch):
    click.echo('Hello, {}!'.format(target_branch))

if __name__ == '__main__':
    gmi()
