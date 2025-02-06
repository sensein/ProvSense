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
from rdflib import Graph

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
def read_file(path):
    with open(path, 'r') as file:
        jsonld_data = json.load(file)
    return json.dumps(jsonld_data)


def detect_rdf_format(data: str):
    """
    Detects whether the given data is in Turtle (TTL), JSON-LD, or N-Triples format.

    Parameters:
        data (str): The RDF data as a string.

    Returns:
        str: The detected format ('turtle', 'json-ld', 'nt', or 'Unknown').

        Example 1:
            Input:
                @prefix ex: <http://example.org/> .
                ex:PersonA ex:name "Alice" .
                ex:PersonA ex:worksAt ex:CompanyY .
                ex:CompanyY ex:location "New York" .
            Output: turtle

        Example 2:
            Input:
                <http://example.org/PersonA> <http://example.org/name> "Alice" .
                <http://example.org/PersonA> <http://example.org/worksAt> <http://example.org/CompanyY> .
                <http://example.org/CompanyY> <http://example.org/location> "New York" .
            Output: nt

        Example 3:
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
            Output: json-ld
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

def _convert_to_nt(input_string):
    """
    Converts an RDF string in JSON-LD or Turtle (TTL) format to N-Triples (NT) format.

    Parameters:
        input_string (str): The input RDF string.

    Returns:
        str: The N-Triples representation of the RDF data.

    Raises:
        ValueError: If the input format is unsupported or cannot be parsed.
    """

    input_type = detect_rdf_format(input_string)

    if input_type == "nt":
        return input_string

    try:
        if input_type == "json-ld":
            return Graph().parse(data=input_string, format='json-ld').serialize(format="nt")
        elif input_type == "turtle":
            return Graph().parse(data=input_string, format='turtle').serialize(format="nt")
        else:
            logging.error((f"Unsupported RDF format detected: {input_type}"))
            raise ValueError(f"Unsupported RDF format detected: {input_type}")

    except Exception as e:
        logging.error(f"Failed to convert input data to N-Triples: {str(e)}")
        raise ValueError(f"Failed to convert RDF data to N-Triples: {str(e)}")

def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].lower()

def convert_single_file_to_nt(input_file):
    """Convert a single JSON-LD or Turtle (TTL)file to ntriple format.
    
    Args:
        file_path (str): Path to the JSON-LD or Turtle (TTL) file
        
    Returns:
        str: In ntriple format
    """
    valid_extensions = {".jsonld", ".ttl", ".nt"}
    if get_file_extension(input_file) not in valid_extensions:
        logger.error(f"Invalid file format={input_file}")
        raise ValueError("File must have a .jsonld, .ttl, or .nt extension.")

    if not os.path.isfile(input_file):
        logging.error(f"File not found: {input_file}")
        raise FileNotFoundError(f"File not found: {input_file}")

    return input_file if get_file_extension(input_file)=="nt" else _convert_to_nt(read_file(input_file))

if __name__ == "__main__":
    input_ttl_data = """
    @prefix ex: <http://example.org/> .
    ex:PersonA ex:name "Alice" .
    ex:PersonA ex:worksAt ex:CompanyY .
    ex:CompanyY ex:location "New York" .
    """
    print("Converting ttl data to ntriples")
    print(_convert_to_nt(input_ttl_data))

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
    print(_convert_to_nt(jsonld_data))

    ntriples_data = """
    <http://example.org/PersonA> <http://example.org/name> "Alice" .
    <http://example.org/PersonA> <http://example.org/worksAt> <http://example.org/CompanyY> .
    <http://example.org/CompanyY> <http://example.org/location> "New York" .
    """
    print("Converting ntriples_data   to ntriples")
    print(_convert_to_nt(ntriples_data))

    input_src_file = "../../example/test_dst.jsonld"
    print("Converting file   to ntriples")
    print(convert_single_file_to_nt(input_src_file))