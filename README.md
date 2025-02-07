# ProvSense

ProvSense is a Python library for managing knowledge graph provenance. It enables efficient comparison of files, tracking changes, and enforcing provenance rules to ensure data integrity and traceability. Ideal for researchers and developers, ProvSense promotes transparency and accountability in data-driven workflows.

## Installation
Install this package via :

```sh
pip install ProvSense
```

Or get the newest development version via:

```sh
pip install git+https://github.com/sensein/ProvSense/.git
```

## Usage
For example files, see `example` directory.

### 1️⃣ Compare Two Knowledge Graph Strings
You can compare two JSON-LD/Turtle/N-Triples formatted knowledge graphs as strings.
```Python
from ProvSense.app import compare_items

# KG string comparison
src = """{ "@context": { "ex": "http://example.org/" }, "@id": "ex:Person1", "@type": "ex:Person", "ex:name": "Alice" }"""

dst = """{ "@context": { "ex": "http://example.org/" }, "@id": "ex:Person1", "@type": "ex:Person", "ex:name": "BoB" }"""

# Compare and print results
print(compare_items(src, dst))

```
**Output:**
```python
[
    {'subject': 'http://example.org/Person1',
  'property': 'http://example.org/name',
  'src_value': 'Alice',
  'dst_value': 'BoB'},
 {'subject': 'http://example.org/Person1',
  'property': 'http://example.org/name',
  'src_value': 'Alice',
  'dst_value': 'BoB'}
]
```

### 2️⃣ Compare Two Knowledge Graph Files
Pass file paths to compare JSON-LD, TTL, or NT files.

```python
from ProvSense.app import compare_items
print(compare_items("test_src.jsonld", "test_dst.jsonld"))

```
**Output:**
```python
[
    {'subject': 'urn:uuid:550e8400-e29b-41d4-a716-446655440000',
  'property': 'http://example.org/worksAt',
  'src_value': 'http://example.org/Company',
  'dst_value': 'http://example.org/CompanyY'},
 {'subject': 'urn:uuid:550e8400-e29b-41d4-a716-446655440000',
  'property': 'http://example.org/worksAt',
  'src_value': 'http://example.org/Company',
  'dst_value': 'http://example.org/CompanyY'},
 {'subject': 'urn:uuid:550e8400-e29b-41d4-a716-446655440000',
  'property': 'http://example.org/location',
  'src_value': None,
  'dst_value': 'New York'}
]

```
### 3️⃣ Compare Two Directories
Compare all JSON-LD, TTL, and NT files in two folders recursively.

Note: The source and destination folders must contain files with matching filenames for a valid comparison.
```python
from ProvSense.app import compare_items
print(compare_items("src", "dst"))
```

**Output:**
```python

{'test_file.jsonld': [{'subject': 'urn:uuid:550e8400-e29b-41d4-a716-446655440000',
   'property': 'http://example.org/worksAt',
   'src_value': 'http://example.org/CompanyX',
   'dst_value': 'http://example.org/CompanyY'},
  {'subject': 'urn:uuid:550e8400-e29b-41d4-a716-446655440000',
   'property': 'http://example.org/location',
   'src_value': None,
   'dst_value': 'New York'},
  {'subject': 'urn:uuid:550e8400-e29b-41d4-a716-446655440000',
   'property': 'http://example.org/worksAt',
   'src_value': 'http://example.org/CompanyX',
   'dst_value': 'http://example.org/CompanyY'}],
 'test_file_b.jsonld': [{'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/Princeton_University',
   'dst_value': 'http://dbpedia.org/resource/ETH_Zurich'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/Princeton_University',
   'dst_value': 'http://dbpedia.org/resource/University_of_Berlin'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/ETH_Zurich',
   'dst_value': 'http://dbpedia.org/resource/Princeton_University'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/ETH_Zurich',
   'dst_value': 'http://dbpedia.org/resource/University_of_Berlin'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/Switzerland',
   'dst_value': 'http://dbpedia.org/resource/Germany'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/Switzerland',
   'dst_value': 'http://dbpedia.org/resource/United_States'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Quantum_mechanics',
   'dst_value': 'http://dbpedia.org/resource/Brownian_motion'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Quantum_mechanics',
   'dst_value': 'http://dbpedia.org/resource/Theory_of_relativity'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/University_of_Berlin',
   'dst_value': 'http://dbpedia.org/resource/Princeton_University'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/University_of_Berlin',
   'dst_value': 'http://dbpedia.org/resource/ETH_Zurich'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/sameAs',
   'src_value': 'https://www.wikidata.org/wiki/Q937',
   'dst_value': 'https://en.wikipedia.org/wiki/Albert_Einstein'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/Germany',
   'dst_value': 'http://dbpedia.org/resource/Switzerland'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/Germany',
   'dst_value': 'http://dbpedia.org/resource/United_States'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Brownian_motion',
   'dst_value': 'http://dbpedia.org/resource/Quantum_mechanics'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Brownian_motion',
   'dst_value': 'http://dbpedia.org/resource/Theory_of_relativity'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/alternateName',
   'src_value': 'Einstein',
   'dst_value': 'Prof. Einstein'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/alternateName',
   'src_value': 'Prof. Einstein',
   'dst_value': 'Einstein'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Theory_of_relativity',
   'dst_value': 'http://dbpedia.org/resource/Quantum_mechanics'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Theory_of_relativity',
   'dst_value': 'http://dbpedia.org/resource/Brownian_motion'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/United_States',
   'dst_value': 'http://dbpedia.org/resource/Switzerland'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/United_States',
   'dst_value': 'http://dbpedia.org/resource/Germany'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/sameAs',
   'src_value': 'https://en.wikipedia.org/wiki/Albert_Einstein',
   'dst_value': 'https://www.wikidata.org/wiki/Q937'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/ETH_Zurich',
   'dst_value': 'http://dbpedia.org/resource/Princeton_University'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/University_of_Berlin',
   'dst_value': 'http://dbpedia.org/resource/Princeton_University'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/Princeton_University',
   'dst_value': 'http://dbpedia.org/resource/ETH_Zurich'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/University_of_Berlin',
   'dst_value': 'http://dbpedia.org/resource/ETH_Zurich'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/Germany',
   'dst_value': 'http://dbpedia.org/resource/Switzerland'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/United_States',
   'dst_value': 'http://dbpedia.org/resource/Switzerland'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Brownian_motion',
   'dst_value': 'http://dbpedia.org/resource/Quantum_mechanics'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Theory_of_relativity',
   'dst_value': 'http://dbpedia.org/resource/Quantum_mechanics'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/Princeton_University',
   'dst_value': 'http://dbpedia.org/resource/University_of_Berlin'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/affiliation',
   'src_value': 'http://dbpedia.org/resource/ETH_Zurich',
   'dst_value': 'http://dbpedia.org/resource/University_of_Berlin'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/sameAs',
   'src_value': 'https://en.wikipedia.org/wiki/Albert_Einstein',
   'dst_value': 'https://www.wikidata.org/wiki/Q937'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/Switzerland',
   'dst_value': 'http://dbpedia.org/resource/Germany'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/United_States',
   'dst_value': 'http://dbpedia.org/resource/Germany'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Quantum_mechanics',
   'dst_value': 'http://dbpedia.org/resource/Brownian_motion'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Theory_of_relativity',
   'dst_value': 'http://dbpedia.org/resource/Brownian_motion'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/alternateName',
   'src_value': 'Prof. Einstein',
   'dst_value': 'Einstein'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/alternateName',
   'src_value': 'Einstein',
   'dst_value': 'Prof. Einstein'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Quantum_mechanics',
   'dst_value': 'http://dbpedia.org/resource/Theory_of_relativity'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/knowsAbout',
   'src_value': 'http://dbpedia.org/resource/Brownian_motion',
   'dst_value': 'http://dbpedia.org/resource/Theory_of_relativity'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/Switzerland',
   'dst_value': 'http://dbpedia.org/resource/United_States'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/nationality',
   'src_value': 'http://dbpedia.org/resource/Germany',
   'dst_value': 'http://dbpedia.org/resource/United_States'},
  {'subject': 'http://dbpedia.org/resource/Albert_Einstein',
   'property': 'http://schema.org/sameAs',
   'src_value': 'https://www.wikidata.org/wiki/Q937',
   'dst_value': 'https://en.wikipedia.org/wiki/Albert_Einstein'},
  {'subject': 'http://dbpedia.org/resource/Brownian_motion',
   'property': 'http://schema.org/name',
   'src_value': 'Brownian',
   'dst_value': 'Brownian Motion'},
  {'subject': 'http://dbpedia.org/resource/Brownian_motion',
   'property': 'http://schema.org/name',
   'src_value': 'Brownian',
   'dst_value': 'Brownian Motion'},
  {'subject': 'http://dbpedia.org/resource/Theory_of_relativity',
   'property': 'http://schema.org/name',
   'src_value': 'Relativity',
   'dst_value': 'Theory of Relativity'},
  {'subject': 'http://dbpedia.org/resource/Theory_of_relativity',
   'property': 'http://schema.org/name',
   'src_value': 'Relativity',
   'dst_value': 'Theory of Relativity'}]}
```

## Running Tests

To run all tests in the project:
```sh
python -m unittest discover src/tests
```

To run a specific test file:
```sh
python -m unittest src/tests/test_ttl_conversion.py
```

To run tests with verbose output:
```sh
python -m unittest -v src/tests/test_ttl_conversion.py
```

