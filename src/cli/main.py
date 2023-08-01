# cli/main.py

import click

from editors import CLIEditorAdapter
from validators import ValidatorConfig
from git import Git
from github import Github


@click.group()
@click.option("-f", "--file", default="doc.md", help="Path to documentation file")
@click.pass_context
def cli(ctx, file):
    """Documentation improvement tool"""
    ctx.obj = {}
    ctx.obj["file"] = file


@cli.command()
@click.option(
    "--validator", default="placeholder", help="Validator to use (default: placeholder)"
)
@click.option(
    "--command", default="cat", help="Command to run on the file (default: cat)"
)
@click.pass_context
def validate(ctx, validator, command):
    """Validate documentation changes"""
    # Get the validator class based on the input
    validator_class = ValidatorConfig.get_validator(validator)

    if not validator_class:
        click.echo(f"Invalid validator: {validator}")
        return

    # Create an instance of the selected validator with the specified command
    validator_instance = validator_class(command)
    issues = validator_instance.validate(ctx.obj["file"])

    if issues:
        click.echo(f"Validation failed with {len(issues)} issue:")
        for issue in issues:
            click.echo(issue)
    else:
        click.echo("Validation succeeded")


@cli.command()
@click.pass_context
def generate_pr(ctx):
    """Generate pull request"""
    git = Git()
    git.commit(ctx.obj["file"])

    github = GitHub()
    github.create_pull_request()


if __name__ == "__main__":
    cli()
