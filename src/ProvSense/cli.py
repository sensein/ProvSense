"""
This module defines CLI commands for the ProvSense application.
"""

import click
from pathlib import Path

@click.group()
@click.pass_context
def cli(ctx):
    """CLI commands for the ProvSense"""
    pass


@cli.command()
@click.option(
    '--source',
    required=True,
    help=(
        "Source path (file/folder) or string (e.g., JSON-LD/TTL) for comparison. "
        "If providing a string, ensure it is properly formatted."
    )
)

@click.option(
    '--destination',
    required=True,
    help=(
        "Destination path (file/folder) or string (e.g., JSON-LD/TTL) for comparison. "
        "If providing a string, ensure it is properly formatted."
    )
)

@click.option(
    '--input_type',
    type=click.Choice(['jsonld', 'ttl'], case_sensitive=False),
    required=True,
    default='file',
    help=(
        "Type of input. Options include:\n"
        "- 'jsonld': Input in JSON-LD format.\n"
        "- 'ttl': Input in Turtle representation.\n"
    )
)


def compare(source: str, destination: str, compare_type:str, input_type: str) -> None:
    """Compare changes in knowledge graph files (JSON-LD, TTL) across different input sources—whether processing multiple files from a folder, a single file, or a direct input string..

    Supports:
    - folder to folder comparison
    - file to file comparison
    - string to string comparison (JSON-LD/TTL)
    """
    try:
        # compare_items(source, destination, type)    to be implemented.
        click.echo(f"Comparing {source} with {destination} as {compare_type} in {input_type} format.")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    cli()