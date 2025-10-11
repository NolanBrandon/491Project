import unittest
import tempfile
import os
from pathlib import Path
import subprocess

# Absolute parser path
PARSER_PATH = Path(__file__).resolve().parents[2] / "cicd_scripts" / "parse_unit_test_results.py"

class TestParseUnitTestResults(unittest.TestCase):
    def setUp(self):
        # Use the real Markdown file for appending Unit Test results
        self.temp_md = Path(__file__).resolve().parents[2] / "docs" / "test_results.md"
        # Ensure the file exists
        if not self.temp_md.exists():
            self.temp_md.touch()

    def test_parser_creates_unit_test_md_entry(self):
        # Create temporary XML file for testing
        temp_xml = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")
        temp_xml_name = temp_xml.name
        temp_xml.close()

        # Example XML content with 2 tests (1 fail, 1 pass)
        xml_content = """<testsuite name="ExampleSuite" tests="2" failures="1" errors="0" skipped="1">
<testcase classname="tests.ExampleTest" name="test_1" time="0.001">
<system-out><![CDATA[PASS Test passed]]></system-out>
</testcase>
<testcase classname="tests.ExampleTest" name="test_2" time="0.001">
<system-out><![CDATA[FAIL Test failed]]></system-out>
</testcase>
</testsuite>"""

        with open(temp_xml_name, "w", encoding="utf-8") as f:
            f.write(xml_content)

        # Run the parser script
        subprocess.run(
            ["python", str(PARSER_PATH), temp_xml_name, str(self.temp_md)],
            check=True
        )

        # Check that Markdown contains the correct Unit Test results
        with open(self.temp_md, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Test Results (Unit Test)", content)
        self.assertIn("- Total tests: 2", content)
        self.assertIn("- Failures: 1", content)
        self.assertIn("- Skipped: 1", content)

        # Clean up temporary XML file
        os.remove(temp_xml_name)

if __name__ == "__main__":
    unittest.main()
