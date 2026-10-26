"""Check the report's business descriptions and one-to-one activity mapping."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'README.md').read_text()
catalog = json.loads((ROOT / 'evidence/use-case-catalog.json').read_text())
ids = {case['id'] for case in catalog}
assert ids == {f'UC{i:02}' for i in range(1, 21)}
assert len({case['bp'] for case in catalog}) == len(catalog)
assert set(re.findall(r'\bUC\d{2}\b', source)) == ids
assert not re.search(r'UC\d{2}[/–-]', source), 'Unexpanded legacy UC reference'
for case in catalog:
    row = f"| {case['bp']} | {case['name']} | {case['id']} |"
    assert source.count(row) == 1, row
    assert source.count(f"| รหัสและชื่อ | {case['id']} {case['name']} |") == 1
section = source[source.index('### 3.4 '):source.index('### 3.5 ')]
for block in re.split(r'(?=#### 3\.4\.\d+ UC)', section)[1:]:
    description = block.split('แผนภาพปฏิสัมพันธ์')[0]
    assert not re.search(r'\b(API|POST|GET|SELECT|INSERT|UPDATE|Service|Repository|Controller|session)\b', description)
    steps = re.findall(r'^\|\s*\|\s*\d+\.', description, re.M)
    assert 2 <= len(steps) <= 4, 'Descriptions must remain compact'
images = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', source)
assert all((ROOT / path).is_file() for path in images)
for case in catalog:
    number = case['id'][2:]
    assert f'(sequence-diagrams/figures/seq-{number}.png)' in source
    assert f'(collaboration-diagrams/figures/collab-{number}.png)' in source
screens = json.loads((ROOT / 'evidence/report-screen-traceability.json').read_text())
assert len(screens) == 33
assert all(set(screen['useCases']) <= ids for screen in screens)
queries = json.loads((ROOT / 'evidence/report-sql-traceability.json').read_text())
assert len(queries) == 24
assert all(set(query['useCases']) <= ids for query in queries)
sequence_source = (ROOT / 'sequence-diagrams/README.md').read_text()
assert len(re.findall(r'^## SEQ-', sequence_source, re.M)) == 23
model = json.loads((ROOT / 'evidence/sql/current20-model.json').read_text())
assert len(model['tables']) == 39 and model['foreignKeys'] == 91
assert len(model['enums']) == 25 and model['migrations'] == 7
assert all(isinstance(e['values'], list) and all(re.fullmatch(r'[a-z_]+', v) for v in e['values']) for e in model['enums'])
dictionary = source[source.index('#### 3.5.4 '):source.index('### 3.6 ')]
assert len(re.findall(r'^##### 3\.5\.4\.\d+ \w+ Table$', dictionary, re.M)) == 39
for table in model['tables']:
    block = re.search(rf'##### 3\.5\.4\.\d+ {table["name"]} Table\n(.*?)(?=\n##### 3\.5\.4\.\d+ |\n#### 3\.5\.5 |\Z)', dictionary, re.S)[1]
    assert set(re.findall(r'^\| `([^`]+)` \| `[^`]+` \|', block, re.M)) == {column['name'] for column in table['columns']}, table['name']
assert not re.search(r'\b[a-f0-9]{64}\b', source), 'Public report must not expose hash sample values'
print(f'PASS: {len(catalog)} BP/UC pairs, compact descriptions, {len(images)} images, 33 screens, 24 query mappings, current39/91/25/7 model')
