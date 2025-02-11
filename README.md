[![progress-banner](https://backend.codecrafters.io/progress/shell/7f79b25b-fbc7-45de-91b1-5cf404401246)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

- [x] Base challenge
- [x] Extension: Navigation
- [x] Extension: Quoting
- [x] Extension: Output Redirection
- [x] Extension: Command Autocompletion

## Challenge

This my Python solutions to the ["Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview).

In this challenge, you'll build your own POSIX compliant shell that's capable of interpreting shell commands, running external programs and builtin commands like cd, pwd, echo and more. Along the way, you'll learn about shell command parsing, REPLs, builtin commands, and more.

## Running program

1. Ensure you have `python (3.11)` installed locally with GNU `readline` (i.e. from pipenv or pyenv, but not system or homebrew).
1. Run `./your_program.sh` to run your program, which is implemented in `app/main.py`.

The code never flushes the stdout buffer, but relies on python being run with `-u` unbuffered flag.

## Extra functionality
- `cd` with no args goes to `$HOME`
- all input (including command) expands unquoted `~` prefix to `$HOME`
- Tab completion filters for if executable bit is set
- Builtins are just exports of the `builtins` module, very low ceremony to add more, and don't need to be aware of stdout redirection.
- Redirection supprts any fd using `dup2`, not just stdout/stderr
- Unit tests for some of the trickier functionality
- Error handling inside `readline` callbacks ensures a raised error will not be swallowed silently.

## Bugs
Command completion doesn't support relative path prefix, e.g. `./your_<TAB>` in current directory.
Completions are only for commands, and don't support arguments.

`type` builtin should ignore folders.

Would be nice to assert no file descriptors / handles are leaked.

Grammar has many edge case, see [POSIX Shell Grammar to potential improvement](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_10_02). e.g. quoted file redirection `echo ">" abc` should print `> abc`.

Depends on `readline` which is not natively supported on Windows. [Workaround](https://stackoverflow.com/a/51964654/771768) is to use `pyreadline3`. Detects the default macOS `readline` and errors (I couldn't get the completion print to work with it).

## Running tests
```bash
python3.11 -m unittest
```
