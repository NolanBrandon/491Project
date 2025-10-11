import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import sys

def parse_xml_to_markdown(xml_file_path, md_file_path):
    xml_file = Path(xml_file_path)
    output_md = Path(md_file_path)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    testsuites = [root] if root.tag == "testsuite" else root.findall("testsuite")

    total = failures = errors = skipped = 0

    for ts in testsuites:
        total += int(ts.attrib.get("tests", 0))
        failures += int(ts.attrib.get("failures", 0))
        errors += int(ts.attrib.get("errors", 0))
        skipped += int(ts.attrib.get("skipped", 0))

    output_md.parent.mkdir(parents=True, exist_ok=True)
    with open(output_md, "a", encoding="utf-8") as f:
        f.write("\n" + "="*60 + "\n")
        f.write(f"# Test Results (Unit Test) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"- Total tests: {total}\n")
        f.write(f"- Failures: {failures}\n")
        f.write(f"- Errors: {errors}\n")
        f.write(f"- Skipped: {skipped}\n")
        f.write("="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parse_unit_test_results.py <xml_file> <output_md_file>")
        sys.exit(1)
    parse_xml_to_markdown(sys.argv[1], sys.argv[2])
