# cli/main.py

import click

from editors import CLIEditorAdapter
from validators import Validator
from git import Git
from github import Github

print("hello, world")

@click.group()
@click.option('-f', '--file', default='doc.md', help='Path to documentation file')
@click.pass_context
def cli(ctx, file):
    """Documentation improvement tool"""
    ctx.obj = {}
    ctx.obj['file'] = file
    

@cli.command()
@click.pass_context
def edit(ctx):
    """Edit documentation file"""
    editor = CLIEditorAdapter()
    content = editor.edit_file(ctx.obj['file'])

    
@cli.command() 
@click.pass_context
def validate(ctx):
    """Validate documentation changes"""
    validator = Validator()
    issues = validator.validate(ctx.obj['file'])

    if issues:
        click.echo(f"Validation failed with {len(issues)} issues")
    else:
        click.echo("Validation succeeded")

    
@cli.command()
@click.pass_context
def generate_pr(ctx):
    """Generate pull request"""
    git = Git() 
    git.commit(ctx.obj['file'])
    
    github = GitHub()
    github.create_pull_request()

if __name__ == '__main__':
    cli()
