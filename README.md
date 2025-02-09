[![progress-banner](https://backend.codecrafters.io/progress/shell/7f79b25b-fbc7-45de-91b1-5cf404401246)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a starting point for Python solutions to the
["Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview).

In this challenge, you'll build your own POSIX compliant shell that's capable of
interpreting shell commands, running external programs and builtin commands like
cd, pwd, echo and more. Along the way, you'll learn about shell command parsing,
REPLs, builtin commands, and more.

## Running program

1. Ensure you have `python (3.11)` installed locally
1. Run `./your_program.sh` to run your program, which is implemented in
   `app/main.py`.

## Extra functionality
- `cd` with no args goes to `$HOME`
- all input (including command) expands `~` to `$HOME`

## Bugs
- quoted arg `"~"` shouldn't be expanded

## Unsure questions
How should `type` function:
- directories -- i.e. `bash: type: /: not found`
- files without executable bit set: i.e. `envvars is /usr/sbin/envvars` but permission is `-rw-r--r--`
