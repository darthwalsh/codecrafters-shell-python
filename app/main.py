import os
import re
import subprocess
import sys

from app import builtins, path


def expand_home(arg):
    if arg.startswith("~"):
        return os.environ["HOME"] + arg[1:]
    return arg


def quote_split(line: str):
    # See https://www.gnu.org/software/bash/manual/bash.html#Quoting for details
    pattern = r"""
(?<!\\)'    # quote not preceded by a backslash
  ([^']*)   # repeated non-quote
'           # closing quote
    |
(?<!\\)"    # double-quote not preceded by a backslash
  (
    (?:\\"  # escaped double-quote
      |
    [^"])   # non-quote
    *       # repeated non-quote
  )
"           # closing double-quote
    |
(\S+)       # plain text
"""

    def escape(single, double, plain):
        if single:
            return single
        if double:
            def replace(match):
                c = match.group(1)
                if c in '$`"\\':
                    return c
                return match.group(0)
            return re.sub(r"\\(.)", replace, double)
        return re.sub(r"\\(.)", r"\1", plain)

    # print(re.findall(pattern, line, re.VERBOSE))
    return [escape(*groups) for groups in re.findall(pattern, line, re.VERBOSE)]


def repl():
    while True:
        sys.stdout.write("$ ")
        try:
            line = input()
        except EOFError:
            return

        command, *args = [expand_home(arg) for arg in quote_split(line)]

        if f := getattr(builtins, command, None):
            f(*args)
        elif path.resolve(command):
            # Don't use resolved path here, as $0 shouldn't be full path for entry in PATH
            subprocess.call([command, *args])
        else:
            print(f"{command}: command not found")


def main():
    repl()


if __name__ == "__main__":
    main()
