import xml.etree.ElementTree as ET
import sys
from datetime import datetime

xml_file = sys.argv[1]
output_md = sys.argv[2]

tree = ET.parse(xml_file)
root = tree.getroot()

# Count tests, failures, errors, skipped
total = int(root.attrib.get('tests', 0))
failures = int(root.attrib.get('failures', 0))
errors = int(root.attrib.get('errors', 0))
skipped = int(root.attrib.get('skipped', 0))

# Append results to Markdown
with open(output_md, 'a', encoding='utf-8') as f:
    f.write(f"\n# Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"- Total tests: {total}\n")
    f.write(f"- Failures: {failures}\n")
    f.write(f"- Errors: {errors}\n")
    f.write(f"- Skipped: {skipped}\n")
