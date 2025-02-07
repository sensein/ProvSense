"""This script defines functions for comparing source with destination.

It provides functionality for folder-to-folder, file-to-file, and string-to-string comparisons.
"""
from pathlib import Path
from typing import Union
import logging
from .shared import compare_graph, convert_to_nt, convert_single_file_to_nt

logger = logging.getLogger(__name__)

def compare_items(source: Union[str, Path], destination: Union[str, Path] ) -> dict:
    """
        Compares the content of `source` and `destination`, which can be file paths
    (to files or directories) or strings representing knowledge graphs (in JSON-LD or TTL format).

    Args:

    -  source (Union[str, Path]): The source item, which can be either:

        - A file or directory path (`Path`).
        - A string representation of a knowledge graph (JSON-LD/TTL).

    - destination (Union[str, Path]): The destination item, which can be either:

        - A file or directory path (`Path`).
        - A string representation of a knowledge graph (JSON-LD/TTL).

    Returns:

     - dict: A dictionary containing the comparison results.

    Notes:

     - If `source` and `destination` are paths, the function will compare their contents.

     - If they are strings, it assumes they are knowledge graphs and processes them accordingly.

     - The function should be extended to include logic for structural or semantic comparisons.

    Example:
        >>> source = '{ "@context": { "ex": "http://example.org/" }, "@id": "ex:Person1", "@type": "ex:Person", "ex:name": "Alice" }'

        >>> destination = '{ "@context": { "ex": "http://example.org/" }, "@id": "ex:Person2", "@type": "ex:Person", "ex:name": "Bob" }'

        >>> compare_items(source, destination)
        {'differences': [...]}

    """

    if isinstance(source, str) and isinstance(destination, str):
        if not (Path(source).exists() or Path(destination).exists()):
            logger.info(f"Comparing strings: {source} with {destination}.")
            return compare_graph(convert_to_nt(source), convert_to_nt(destination))

    # Convert to Path objects if they're strings
    src = Path(source) if isinstance(source, str) else source
    dst = Path(destination) if isinstance(destination, str) else destination

    # Validate existence
    if not src.exists():
        logger.error(f"Source path does not exist: {source}")
        raise FileNotFoundError(f"Source path does not exist: {source}")
    if not dst.exists():
        logger.error(f"Destination path does not exist: {destination}")
        raise FileNotFoundError(f"Destination path does not exist: {destination}")
    
    # Handle file to file comparison
    if src.is_file() and dst.is_file():
        logger.info(f"Comparing files: {src} with {dst}.")
        return compare_graph(convert_single_file_to_nt(source), convert_single_file_to_nt(destination))

    elif src.is_dir() and dst.is_dir():
        logger.info(f"Comparing directories: {src} with {dst}.")
        differences = {}

        valid_extensions = {".jsonld", ".ttl", ".nt"}

        src_files = {f.name: f for f in src.glob("*") if f.is_file() and f.suffix in valid_extensions}
        dst_files = {f.name: f for f in dst.glob("*") if f.is_file() and f.suffix in valid_extensions}

        # Compare matching files
        for filename in src_files.keys() | dst_files.keys():  # Union of both file sets
            src_file = src_files.get(filename)
            dst_file = dst_files.get(filename)

            if src_file and dst_file:
                logger.info(f"Processing files: {src_file} with {dst_file}")
                differences[filename] = compare_graph(
                    convert_single_file_to_nt(src_file),
                    convert_single_file_to_nt(dst_file),
                )
            elif src_file and not dst_file:
                logger.warning(f"File missing in destination: {filename}")
                differences[filename] = {"status": "missing in destination"}
            elif dst_file and not src_file:
                logger.warning(f"File missing in source: {filename}")
                differences[filename] = {"status": "missing in source"}

        return differences
    else:
        logger.error("Source and destination must be of the same type (both files, both folders, or both strings)")
        raise ValueError("Source and destination must be of the same type (both files, both folders, or both strings)")


