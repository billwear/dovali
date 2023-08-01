# editors.py

import click
import tempfile
import os

class Editor:
    """Editor interface"""

    def __init__(self):
        pass

    def get():
        return Editor()

    def edit_file(self, file_path):
        """Edit the specified file using the built-in editor"""
        click.echo(f"Opening {file_path} for editing...")
        click.edit(filename=file_path)
        click.echo(f"{file_path} has been edited.")

class CLIEditorAdapter:
    """CLI editor adapter for printing the document to console"""

    def __init__(self):
        pass

    def edit_file(self, file_path):
        """Edit the file using the built-in editor and print the content"""
        click.echo(f"Opening {file_path} for editing...")
        click.edit(filename=file_path)
        click.echo(f"{file_path} has been edited. Here is the current content:")
        with open(file_path, 'r') as file:
            content = file.read()
            click.echo(content)
