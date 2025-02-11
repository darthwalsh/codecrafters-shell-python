from dataclasses import dataclass
import os
import re
import subprocess
import sys
from typing import Self

from app import builtins, path
from app.command import Command


def repl():
    # https://www.gnu.org/software/bash/manual/bash.html#Shell-Operation
    while True:
        sys.stdout.write("$ ")
        try:
            line = input()
        except EOFError:
            return

        expanded = [expand(arg) for arg in quote_split(line)]
        cmd = Command.parse(expanded)

        with cmd.redirect():
            """Set up redirects before calling any builtins"""
            if f := getattr(builtins, cmd.command, None):
                f(*cmd.args)
            elif path.resolve(cmd.command):
                # Don't use resolved path here, as $0 shouldn't be full path for entry in PATH
                subprocess.call([cmd.command, *cmd.args])
            else:
                print(f"{cmd.command}: command not found")


@dataclass
class Token:
    text: str
    quoted: bool

    @staticmethod
    def plain(text: str) -> Self:
        return Token(text, False)

    @staticmethod
    def quote(text: str) -> Self:
        return Token(text, True)


def quote_split(line: str) -> list[Token]:
    # https://www.gnu.org/software/bash/manual/bash.html#Quoting
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

    def escape(single, double, plain) -> Token:
        if single:
            return Token.quote(single)

        if double:

            def replace(match):
                c = match.group(1)
                if c in '$`"\\':
                    return c
                return match.group(0)

            return Token.quote(re.sub(r"\\(.)", replace, double))
        return Token.plain(re.sub(r"\\(.)", r"\1", plain))

    args: list[Token] = []
    for spaces, single, double, plain in re.findall(pattern, line, re.VERBOSE):
        content = escape(single, double, plain)
        if spaces or not args:
            args.append(content)
        else:
            args[-1].text += content.text
    return args


def expand(arg: Token) -> str:
    text = arg.text
    # https://www.gnu.org/software/bash/manual/bash.html#Shell-Expansions
    # NOT_IMPLEMENTED: brace expansion
    if not arg.quoted:
        text = expand_home(text)
    # NOT_IMPLEMENTED: parameter and variable expansion
    # NOT_IMPLEMENTED: command substitution
    # NOT_IMPLEMENTED: arithmetic expansion
    # NOT_IMPLEMENTED: word splitting
    # NOT_IMPLEMENTED: filename expansion
    return text


def expand_home(arg: str):
    if arg.startswith("~"):
        return os.environ["HOME"] + arg[1:]
    return arg


def main():
    repl()


if __name__ == "__main__":
    main()
