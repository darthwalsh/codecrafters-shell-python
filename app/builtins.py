import sys


def exit(code, *_):
    sys.exit(int(code))


def echo(*args):
    print(*args)


def type(name, *_):
    if name in globals():
        print(f"{name} is a shell builtin")
    else:
        print(f"{name}: not found")
