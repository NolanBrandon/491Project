import xml.etree.ElementTree as ET
import sys
from datetime import datetime

xml_file = sys.argv[1]
output_md = sys.argv[2]

tree = ET.parse(xml_file)
root = tree.getroot()

# Collect failed test info
failures = []
for testcase in root.iter('testcase'):
    for failure in testcase.findall('failure'):
        failures.append({
            'test': testcase.attrib.get('classname') + "." + testcase.attrib.get('name'),
            'message': failure.attrib.get('message') or failure.text
        })

# Append to Markdown
with open(output_md, 'a', encoding='utf-8') as f:
    f.write(f"\n# Bug Tracking - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    if not failures:
        f.write("No test failures. All tests passed ✅\n")
    else:
        for i, bug in enumerate(failures, 1):
            f.write(f"## Bug {i}\n")
            f.write(f"**Test:** {bug['test']}\n\n")
            f.write(f"**Failure Message:**\n```\n{bug['message']}\n```\n\n")
