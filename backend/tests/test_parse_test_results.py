import unittest
import tempfile
import os
from pathlib import Path
import subprocess

# Path to the unit test parser
PARSER_PATH = Path(__file__).resolve().parents[2] / "cicd_scripts" / "parse_unit_test_results.py"


class TestParseUnitTestResults(unittest.TestCase):
    def setUp(self):
        # Temporary Markdown file for results
        self.temp_md = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".md")
        self.temp_md.close()
        
        # XML templates
        self.xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="{name}" tests="{tests}" failures="{failures}" errors="{errors}" skipped="{skipped}">
{testcases}
</testsuite>
"""
        self.testcase_template = """<testcase classname="{classname}" name="{name}" time="0.001">
<system-out><![CDATA[{status}]]></system-out>
</testcase>
"""

    def tearDown(self):
        os.remove(self.temp_md.name)

    def _write_xml(self, filename, name="ExampleSuite", tests=3, failures=1, errors=0, skipped=1):
        testcases = ""
        for i in range(tests):
            if i < failures:
                status = "FAIL Test failed"
            elif i < failures + skipped:
                status = "SKIPPED Test skipped"
            else:
                status = "PASS Test passed"
            testcases += self.testcase_template.format(classname="tests.ExampleTest", name=f"test_{i}", status=status)
        content = self.xml_template.format(name=name, tests=tests, failures=failures, errors=errors, skipped=skipped, testcases=testcases)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    def test_unit_parser_appends_results(self):
        # Create temporary XML file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_xml:
            temp_xml_name = temp_xml.name
        self._write_xml(temp_xml_name, tests=5, failures=2, errors=1, skipped=1)

        # Run the unit test parser
        subprocess.run(
            ["python", str(PARSER_PATH), temp_xml_name, self.temp_md.name],
            check=True
        )

        # Read Markdown output
        with open(self.temp_md.name, "r", encoding="utf-8") as f:
            content = f.read()

        # Verify counts
        self.assertIn("- Total tests: 5", content)
        self.assertIn("- Failures: 2", content)
        self.assertIn("- Errors: 1", content)
        self.assertIn("- Skipped: 1", content)
        # Verify the Markdown shows 'Unit Test'
        self.assertIn("Test Results (Unit Test)", content)

        # Clean up temporary XML
        os.remove(temp_xml_name)

    def test_unit_parser_multiple_runs(self):
        # First run
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_xml1:
            temp_xml_name1 = temp_xml1.name
        self._write_xml(temp_xml_name1, tests=3, failures=0, errors=0, skipped=0)

        subprocess.run(
            ["python", str(PARSER_PATH), temp_xml_name1, self.temp_md.name],
            check=True
        )

        # Second run
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_xml2:
            temp_xml_name2 = temp_xml2.name
        self._write_xml(temp_xml_name2, tests=4, failures=1, errors=0, skipped=2)

        subprocess.run(
            ["python", str(PARSER_PATH), temp_xml_name2, self.temp_md.name],
            check=True
        )

        # Read Markdown
        with open(self.temp_md.name, "r", encoding="utf-8") as f:
            content = f.read()

        # Ensure both runs are present
        self.assertIn("- Total tests: 3", content)
        self.assertIn("- Total tests: 4", content)
        self.assertIn("Test Results (Unit Test)", content)

        # Clean up XMLs
        os.remove(temp_xml_name1)
        os.remove(temp_xml_name2)


if __name__ == "__main__":
    unittest.main()
