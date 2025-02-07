import unittest
from unittest.mock import patch, mock_open
import os
from ProvSense.shared import _convert_to_nt, convert_single_file_to_nt

class TestNTriplesConversion(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.test_jsonld_str = """{
            "@context": {
                "@vocab": "http://example.org/"
            },
            "@type": "Person",
            "@id": "http://example.org/PersonA",
            "name": "Alice",
            "worksAt": { "@id": "http://example.org/CompanyY" }
        }"""

        self.test_ttl_str = """
@prefix ex: <http://example.org/> .
ex:PersonA a ex:Person ;
    ex:name "Alice" ;
    ex:worksAt ex:CompanyY .
"""

        self.test_ntriples_str = """<http://example.org/PersonA> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Person> .
<http://example.org/PersonA> <http://example.org/name> "Alice" .
<http://example.org/PersonA> <http://example.org/worksAt> <http://example.org/CompanyY> ."""

    def test_convert_jsonld_to_nt(self):
        """Test converting JSON-LD to N-Triples"""
        result = _convert_to_nt(self.test_jsonld_str)
        self.assertIsInstance(result, str)
        expected_triples = {
            "<http://example.org/PersonA> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Person>",
            "<http://example.org/PersonA> <http://example.org/name> \"Alice\"",
            "<http://example.org/PersonA> <http://example.org/worksAt> <http://example.org/CompanyY>"
        }
        result_triples = {line.strip(' .') for line in result.strip().split('\n') if line.strip()}
        self.assertEqual(expected_triples, result_triples)

    def test_convert_ttl_to_nt(self):
        """Test converting TTL to N-Triples"""
        result = _convert_to_nt(self.test_ttl_str)
        self.assertIsInstance(result, str)
        expected_triples = {
            "<http://example.org/PersonA> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Person>",
            "<http://example.org/PersonA> <http://example.org/name> \"Alice\"",
            "<http://example.org/PersonA> <http://example.org/worksAt> <http://example.org/CompanyY>"
        }
        result_triples = {line.strip(' .') for line in result.strip().split('\n') if line.strip()}
        self.assertEqual(expected_triples, result_triples)

    def test_convert_nt_to_nt(self):
        """Test converting N-Triples to N-Triples (should return the same format)"""
        result = _convert_to_nt(self.test_ntriples_str)
        self.assertIsInstance(result, str)
        expected_triples = {line.strip(' .') for line in self.test_ntriples_str.strip().split('\n') if line.strip()}
        result_triples = {line.strip(' .') for line in result.strip().split('\n') if line.strip()}
        self.assertEqual(expected_triples, result_triples)

    def test_convert_single_file_to_nt(self):
        """Test converting a single JSON-LD file to N-Triples"""
        # Create a temporary test file
        test_file = "test_temp.jsonld"
        try:
            with open(test_file, 'w') as f:
                f.write(self.test_jsonld_str)
            
            result = convert_single_file_to_nt(test_file)
            self.assertIsInstance(result, str)
            expected_triples = {
                "<http://example.org/PersonA> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Person>",
                "<http://example.org/PersonA> <http://example.org/name> \"Alice\"",
                "<http://example.org/PersonA> <http://example.org/worksAt> <http://example.org/CompanyY>"
            }
            result_triples = {line.strip(' .') for line in result.strip().split('\n') if line.strip()}
            self.assertEqual(expected_triples, result_triples)
        finally:
            # Clean up the temporary file
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_convert_single_file_not_found(self):
        """Test file not found error for single file conversion"""
        with self.assertRaises(FileNotFoundError):
            convert_single_file_to_nt("nonexistent.jsonld")

    def test_convert_single_file_invalid_extension(self):
        """Test invalid file extension error for single file conversion"""
        with self.assertRaises(ValueError):
            convert_single_file_to_nt("test.txt")

if __name__ == '__main__':
    unittest.main()
