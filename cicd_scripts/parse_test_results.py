import xml.etree.ElementTree as ET
import sys
from datetime import datetime
from pathlib import Path

# Command line arguments
xml_file = sys.argv[1]
output_md = Path(sys.argv[2])

# Ensure the docs folder exists
output_md.parent.mkdir(parents=True, exist_ok=True)

# Parse XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Sum counts from all <testsuite> elements
total = sum(int(ts.attrib.get('tests', 0)) for ts in root.findall('testsuite'))
failures = sum(int(ts.attrib.get('failures', 0)) for ts in root.findall('testsuite'))
errors = sum(int(ts.attrib.get('errors', 0)) for ts in root.findall('testsuite'))
skipped = sum(int(ts.attrib.get('skipped', 0)) for ts in root.findall('testsuite'))

# Append results to Markdown with a timestamp
with open(output_md, 'a', encoding='utf-8') as f:
    f.write("\n" + "="*50 + "\n")
    f.write(f"# Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"- Total tests: {total}\n")
    f.write(f"- Failures: {failures}\n")
    f.write(f"- Errors: {errors}\n")
    f.write(f"- Skipped: {skipped}\n")
