import sys

from app import path


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
