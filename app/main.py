import sys

def repl():
    while True:
        sys.stdout.write("$ ")
        command, *args = input().split()
        match command:
            case "exit":
                sys.exit(int(args[0]))
            case _:
                print(f"{command}: command not found")


def main():
    repl()


if __name__ == "__main__":
    main()
