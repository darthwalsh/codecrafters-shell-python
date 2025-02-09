import os
import subprocess
import sys

from app import builtins, path


def expand_home(arg):
    if arg.startswith("~"):
        return os.environ["HOME"] + arg[1:]
    return arg


def repl():
    while True:
        sys.stdout.write("$ ")
        try:
            line = input()
        except EOFError:
            return

        command, *args = [expand_home(arg) for arg in line.split()]

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
