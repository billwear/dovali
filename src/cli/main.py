# cli/main.py

import click

from editors import CLIEditorAdapter
from validators import ValidatorConfig
from git import Git
from github import Github

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
    editor = Editor()
    editor.edit_file(ctx.obj['file'])

@cli.command()
@click.option('--validator', default='placeholder', help='Validator to use (default: placeholder)')
@click.pass_context
def validate(ctx, validator):
    """Validate documentation changes"""
    # Get the validator class based on the input
    validator_class = ValidatorConfig.get_validator(validator)
    
    if not validator_class:
        click.echo(f"Invalid validator: {validator}")
        return

    # Create an instance of the selected validator and perform validation
    validator_instance = validator_class()
    issues = validator_instance.validate(ctx.obj['file'])

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
