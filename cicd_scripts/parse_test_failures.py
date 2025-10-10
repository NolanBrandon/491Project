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

# Collect failed test info from all testsuites
failures = []
for ts in root.findall('testsuite'):
    for testcase in ts.findall('testcase'):
        for failure in testcase.findall('failure'):
            failures.append({
                'test': testcase.attrib.get('classname', 'Unknown') + "." + testcase.attrib.get('name', 'Unknown'),
                'message': failure.attrib.get('message') or failure.text
            })

# Append to Markdown with timestamp
with open(output_md, 'a', encoding='utf-8') as f:
    f.write("\n" + "="*50 + "\n")
    f.write(f"# Bug Tracking - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    if not failures:
        f.write("No test failures. All tests passed ✅\n")
    else:
        for i, bug in enumerate(failures, 1):
            f.write(f"## Bug {i}\n")
            f.write(f"**Test:** {bug['test']}\n\n")
            f.write(f"**Failure Message:**\n```\n{bug['message']}\n```\n\n")
