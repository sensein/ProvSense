# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# DISCLAIMER: This software is provided "as is" without any warranty,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose, and non-infringement.
#
# In no event shall the authors or copyright holders be liable for any
# claim, damages, or other liability, whether in an action of contract,
# tort, or otherwise, arising from, out of, or in connection with the
# software or the use or other dealings in the software.
# -----------------------------------------------------------------------------

# @Author  : Tek Raj Chhetri
# @Email   : tekraj@mit.edu
# @Web     : https://tekrajchhetri.com/
# @File    : shared.py
# @Software: PyCharm


import logging
import os
import json
from rdflib import Graph, ConjunctiveGraph
from rdflib.query import Result

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

import os

def read_file(path):
    """
    Read the content of a file (JSON-LD, Turtle, or N-Triples) and return it as a string.

    This function reads the file as plain text, regardless of its format.
    It supports JSON-LD (.jsonld), Turtle (.ttl), and N-Triples (.nt) files.

    Args:
        path (str): The file path to the RDF file.

    Returns:
        str: The raw content of the file as a string.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file format is unsupported.

    Example:
        >>> with open("example.jsonld", "w") as f:
        ...     f.write('{"@context": "http://schema.org", "name": "Alice"}')

        >>> read_file("example.jsonld")
        '{"@context": "http://schema.org", "name": "Alice"}'
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    # Determine file format based on extension
    file_extension = os.path.splitext(path)[1].lower()
    if file_extension not in {'.jsonld', '.ttl', '.nt'}:
        raise ValueError(f"Unsupported file format: {file_extension}")

    # Read file content
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

def detect_rdf_format(data: str):
    """
    Detect the format of a given RDF data string.

    This function analyzes the provided RDF string and determines whether it is in
    Turtle (TTL), JSON-LD, or N-Triples (NT) format. If the format cannot be identified,
    it returns 'Unknown'.

    Args:
        data (str): The RDF data as a string.

    Returns:
        str: The detected format, which can be one of the following:
            - 'turtle' for Turtle (TTL) format.
            - 'json-ld' for JSON-LD format.
            - 'nt' for N-Triples (NT) format.
            - 'Unknown' if the format cannot be determined.

    Examples:
        Example 1 (Turtle format):
            Input:
                @prefix ex: <http://example.org/> .
                ex:PersonA ex:name "Alice" .
                ex:PersonA ex:worksAt ex:CompanyY .
                ex:CompanyY ex:location "New York" .
            Output:
                'turtle'

        Example 2 (N-Triples format):
            Input:
                <http://example.org/PersonA> <http://example.org/name> "Alice" .
                <http://example.org/PersonA> <http://example.org/worksAt> <http://example.org/CompanyY> .
                <http://example.org/CompanyY> <http://example.org/location> "New York" .
            Output:
                'nt'

        Example 3 (JSON-LD format):
            Input:
               {
                  "@context": "http://example.org/",
                  "@id": "urn:uuid:550e8400-e29b-41d4-a716-446655440000",
                  "@type": "Person",
                  "name": "Alice",
                  "worksAt": {
                    "@id": "CompanyY"
                  }
               }
            Output:
                'json-ld'
    """
    logger.info("Checking the input types, i.e, whether it is ttl, json-ld or nt")

    # try to read Ntriple string
    # Note the order is important particularly for nt and ttl, so do not move this code.
    try:
        graph = Graph()
        graph.parse(data=data, format="nt")
        return "nt"
    except Exception:
        pass  # Not N-Triples

    # try to read json-ld string
    try:
        json_data = json.loads(data)
        if isinstance(json_data, dict) and any(key in json_data for key in ["@context", "@id", "@type", "@graph"]):
            return "json-ld"
    except json.JSONDecodeError:
        pass  # Not JSON-LD, continue checking other formats

    # Try parsing as Turtle to check if the input string is in turtle data
    try:
        graph = Graph()
        graph.parse(data=data, format="turtle")
        return "turtle"
    except Exception:
        pass  # Not TTL, continue checking

    return "Unknown"

def convert_to_nt(input_string):
    """
    Convert an RDF string from JSON-LD or Turtle (TTL) format to N-Triples (NT) format.

    This function takes an RDF string in either JSON-LD or Turtle format, parses its contents,
    and converts it into the N-Triples format, a line-based RDF serialization.

    Args:
        input_string (str): The RDF data as a string in JSON-LD or Turtle format.

    Returns:
        str: The RDF data converted into N-Triples format.

    Raises:
        ValueError: If the input format is unsupported or the RDF data cannot be parsed.
    """


    input_type = detect_rdf_format(input_string)

    if input_type == "nt":
        return input_string

    try:
        if input_type == "json-ld" or input_type == "turtle":
            return Graph().parse(data=input_string, format=input_type).serialize(format="nt")
        else:
            logging.error((f"Unsupported RDF format detected: {input_type}"))
            raise ValueError(f"Unsupported RDF format detected: {input_type}")

    except Exception as e:
        logging.error(f"Failed to convert input data to N-Triples: {str(e)}")
        raise ValueError(f"Failed to convert RDF data to N-Triples: {str(e)}")

def get_file_extension(file_name):
    """
    Extract the file extension from a given file name.

    This function retrieves the file extension (including the dot) from the provided file name
    and returns it in lowercase.

    Args:
        file_name (str): The name of the file, including its extension.

    Returns:
        str: The file extension in lowercase (e.g., '.txt', '.json', '.ttl').
              Returns an empty string if no extension is found.

    Example:
        >>> get_file_extension("example.json")
        '.json'

        >>> get_file_extension("document.TTL")
        '.ttl'

        >>> get_file_extension("no_extension")
        ''
    """

    return os.path.splitext(file_name)[1].lower()

def convert_single_file_to_nt(input_file):
    """
    Convert a JSON-LD or Turtle (TTL) file to N-Triples (N-Triples) format.

    This function reads a given JSON-LD or TTL file, processes its RDF data, and converts it into
    the N-Triples format, which is a line-based RDF serialization.

    Args:
        file_path (str): The path to the input file, which must be in JSON-LD or Turtle format.

    Returns:
        str: A string representation of the RDF data in N-Triples format.
    """
    valid_extensions = {".jsonld", ".ttl", ".nt"}
    if get_file_extension(input_file) not in valid_extensions:
        logger.error(f"Invalid file format={input_file}")
        raise ValueError("File must have a .jsonld, .ttl, or .nt extension.")

    if not os.path.isfile(input_file):
        logging.error(f"File not found: {input_file}")
        raise FileNotFoundError(f"File not found: {input_file}")

    return input_file if get_file_extension(input_file)=="nt" else convert_to_nt(read_file(input_file))

def compare_graph(source: str, destination: str) -> list[dict]:
    """
    Compares two RDF graphs represented in N-Triples format and identifies differences.

    The function creates two named graphs (`src` and `dst`) using fixed IRIs:
    - `http://graphcompare.org/src` for the source graph
    - `http://graphcompare.org/dst` for the destination graph

    It then runs a SPARQL query to detect differences between the graphs.

    Args:
        source (str): RDF graph in N-Triples format representing the source dataset.
        destination (str): RDF graph in N-Triples format representing the destination dataset.

    Returns:

     - list[dict]: A list of dictionaries representing the differences found between the graphs.
                    Each dictionary contains:
                    - `subject`: The subject of the differing triple.
                    - `property`: The predicate/property of the differing triple.
                    - `src_value`: The object value from the source graph (if available).
                    - `dst_value`: The object value from the destination graph (if available).

    Sample output
    ```Python
          [{'subject': 'urn:uuid:550e8400-e29b-41d4-a716-446655440000',
          'property': 'http://example.org/worksAt',
          'src_value': 'http://example.org/CompanyX1',
          'dst_value': 'http://example.org/CompanyY'},
         {'subject': 'urn:uuid:550e8400-e29b-41d4-a716-446655440000',
          'property': 'http://example.org/location',
          'src_value': None,
          'dst_value': 'New York'},
         {'subject': 'urn:uuid:550e8400-e29b-41d4-a716-446655440000',
          'property': 'http://example.org/worksAt',
          'src_value': 'http://example.org/CompanyX1',
          'dst_value': 'http://example.org/CompanyY'}]
    ```
    """
    g = ConjunctiveGraph()

    # Create named graphs for comparison
    g_src = g.get_context("http://graphcompare.org/src")
    g_src.parse(data=source, format="nt")

    g_dst = g.get_context("http://graphcompare.org/dst")
    g_dst.parse(data=destination, format="nt")


    results: Result = g.query(construct_diff_sparql_query())

    # Convert results to a list of dictionaries
    result_list = [
        {
            "subject": str(row.subject),
            "property": str(row.property),
            "src_value": str(row.srcGraphValue) if row.srcGraphValue else None,
            "dst_value": str(row.dstGraphValue) if row.dstGraphValue else None,
        }
        for row in results
    ]

    return result_list

def construct_diff_sparql_query():
    """
        Constructs a SPARQL query to compare RDF triples from two named graphs:
        a source graph (`src`) and a destination graph (`dst`). The query identifies
        triples that differ between the two graphs, including:

        - Triples present in the source graph but either missing or different in the destination graph.
        - Triples present in the destination graph but either missing or different in the source graph.

        The query retrieves the following variables:
        - `?subject`: The subject of the triple.
        - `?property`: The predicate/property of the triple.
        - `?srcGraphValue`: The object value from the source graph (if available).
        - `?dstGraphValue`: The object value from the destination graph (if available).

        The results are ordered by `?subject`.

        Returns:
            str: The SPARQL query as a string.
        """
    query = """
    PREFIX gcp: <http://graphcompare.org/>
    SELECT ?subject ?property ?srcGraphValue ?dstGraphValue
    WHERE {
        {
            GRAPH <http://graphcompare.org/src> { ?subject ?property ?srcGraphValue }
            OPTIONAL { GRAPH <http://graphcompare.org/dst> { ?subject ?property ?dstGraphValue } }
            FILTER (!BOUND(?dstGraphValue) || ?srcGraphValue != ?dstGraphValue) 
        }
        UNION
        {
            GRAPH <http://graphcompare.org/dst> { ?subject ?property ?dstGraphValue }
            OPTIONAL { GRAPH <http://graphcompare.org/src> { ?subject ?property ?srcGraphValue } }
            FILTER (!BOUND(?srcGraphValue) || ?srcGraphValue != ?dstGraphValue) 
        }
    }
    ORDER BY ?subject
    """
    return query

if __name__ == "__main__":
    input_ttl_data = """
    @prefix ex: <http://example.org/> .
    ex:PersonA ex:name "Alice" .
    ex:PersonA ex:worksAt ex:CompanyY .
    ex:CompanyY ex:location "New York" .
    """
    print("Converting ttl data to ntriples")
    print(convert_to_nt(input_ttl_data))

    jsonld_data = """
    {
      "@context": "http://example.org/",
      "@id": "urn:uuid:550e8400-e29b-41d4-a716-446655440000",
      "@type": "Person",
      "name": "Alice",
      "worksAt": {
        "@id": "CompanyY"
      }
    }
    """
    print("Converting jsonld data to ntriples")
    print(convert_to_nt(jsonld_data))

    ntriples_data = """
    <http://example.org/PersonA> <http://example.org/name> "Alice" .
    <http://example.org/PersonA> <http://example.org/worksAt> <http://example.org/CompanyY> .
    <http://example.org/CompanyY> <http://example.org/location> "New York" .
    """
    print("Converting ntriples_data   to ntriples")
    print(convert_to_nt(ntriples_data))

    input_src_file = "../../example/test_dst.jsonld"
    print("Converting file   to ntriples")
    print(convert_single_file_to_nt(input_src_file))

    input_src_ttl_file = "../../example/test_data.ttl"
    print("Converting ttl file   to ntriples")
    print(convert_single_file_to_nt(input_src_ttl_file))