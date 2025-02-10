import os
from pathlib import Path
import sys

from app import path


# See https://www.gnu.org/software/bash/manual/bash.html#Bourne-Shell-Builtins


def exit(code, *_):
    sys.exit(int(code))


def echo(*args):
    print(*args)


def type(name, *_):
    if name in globals():
        print(f"{name} is a shell builtin")
    elif resolved := path.resolve(name):
        print(f"{name} is {resolved}")
    else:
        print(f"{name}: not found")


def pwd(*_):
    print(Path.cwd())


def cd(*args):
    if not args:
        args = [os.environ["HOME"]]

    dir = args[0]
    try:
        os.chdir(dir)
    except FileNotFoundError:
        print(f"cd: {dir}: No such file or directory")
