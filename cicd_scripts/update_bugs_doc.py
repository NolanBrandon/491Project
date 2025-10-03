import sys
import xml.etree.ElementTree as ET
from datetime import datetime

xml_file = sys.argv[1]
bugs_md = sys.argv[2]

tree = ET.parse(xml_file)
root = tree.getroot()

failures = []
for testcase in root.iter('testcase'):
    if testcase.find('failure') is not None:
        failures.append(testcase.attrib['name'])

if failures:
    with open(bugs_md, 'a') as f:
        f.write(f"## Bugs found on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        for test in failures:
            f.write(f"- {test}\n")
        f.write("\n")
