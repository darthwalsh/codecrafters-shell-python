import sys

from app import builtins


def repl():
    while True:
        sys.stdout.write("$ ")
        command, *args = input().split()

        def command_not_found(*_):
            print(f"{command}: command not found")

        f = getattr(builtins, command, command_not_found)
        f(*args)


def main():
    repl()


if __name__ == "__main__":
    main()
