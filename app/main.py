import sys


def repl():
    while True:
        sys.stdout.write("$ ")
        command = input()
        print(f"{command}: command not found")


def main():
    repl()


if __name__ == "__main__":
    main()
