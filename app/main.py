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
(\s*)         # preceding whitespace
(?:
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
  (           # PLAIN segment
    (?:
      (?:     # either \. or any non-quote non-whitespace
        \\.    # escaped anything
        |
        (?!['"])# Not a quote
        \S      # plain text
      )
    )+        # repeated (not really necessary, but avoid looping below)
  )
)
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

    args = []
    for spaces, single, double, plain in re.findall(pattern, line, re.VERBOSE):
        content = escape(single, double, plain)
        if spaces or not args:
            args.append(content)
        else:
            args[-1] += content
    return args


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
