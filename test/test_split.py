from pathlib import Path
import subprocess
import unittest

from app.main import quote_split

splitter = Path(__file__).parent / "splitter"


def get_expected(args):
    """Use the real shell to see how args are joined"""
    # If this raises, then the test is invalid
    return subprocess.check_output(f"{splitter} {args}", shell=True).decode()


CASES = """
plain

'single quote'
"double quote"
"mixed 'quote"
'mixed "quote'
"extra     spaces"
plain \\"escaped
plain escaped\\"
plain escaped\\"quote
double "\\"escaped"
double "\\'escaped"
double "\\\\escaped"
double "\\" backslash"
non-special\\t escape
'script     test' 'hello''example'
"double"plain'single'
plain"double"'single'
'single'plain"double"
""".strip().splitlines()


class TestQuoteSplit(unittest.TestCase):
    def test_cases(self):
        for case in CASES:
            with self.subTest(line=case):
                actual = "|".join(t.text for t in quote_split(case))
                self.assertEqual(actual, get_expected(case))


if __name__ == "__main__":
    unittest.main()
