from pathlib import Path
import subprocess
import unittest

from app.main import quote_split

splitter = Path(__file__).parent / "splitter"


class HaltingTestCase(unittest.TestCase):
    def run(self, result=None):
        """Stop after first error"""
        if not result.errors:
            super(HaltingTestCase, self).run(result)


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
""".strip().splitlines()

# BUG parses `"ab"c`` to two args


class TestQuoteSplit(HaltingTestCase):
    def test_cases(self):
        for case in CASES:
            with self.subTest(line=case):
                print(case)
                actual = "|".join(quote_split(case))
                self.assertEqual(actual, get_expected(case))


if __name__ == "__main__":
    unittest.main()
