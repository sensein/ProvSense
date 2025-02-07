"""
This module defines CLI commands for the ProvSense application.
"""

import click
from .app import compare_items

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


def compare(source: str, destination: str) -> dict:
    """
        Compare changes in knowledge graph files (JSON-LD, Turtle) across different input sources.

        This function detects and analyzes differences between RDF data sources, supporting comparisons
        at the folder, file, or direct string level.

        Options:

        - --source (str):
                The first input source, which can be a folder path, file path, or RDF string.
                If providing a string, ensure it is correctly formatted in JSON-LD or Turtle.

        - --destination (str):
                The second input source, which can be a folder path, file path, or RDF string.
                If providing a string, ensure it is correctly formatted in JSON-LD or Turtle.

        Returns:
            dict: A dictionary containing the comparison results highlighting the differences.

        Raises:
            FileNotFoundError: If the specified folder or file does not exist.
            ValueError: If an unsupported input type is provided.

        Example Usage:
          - Compare two folders:

           `$ cli compare --source "folder1" --destination "folder2"`

          - Compare two files:

            `$ cli compare --source "file1.ttl" --destination "file2.ttl"`

          - Compare two RDF strings:

            `$ cli compare --source '{"@context": "http://schema.org", "name": "Alice"}' --destination '{"@context": "http://schema.org", "name": "Bob"}'`
        """
    result =  compare_items(source=source, destination=destination)
    click.echo(result)

    try:
        # compare_items(source, destination, type)    to be implemented.
        click.echo(f"Comparing {source} with {destination}.")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    cli()