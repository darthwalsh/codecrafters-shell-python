import readline

from app.path import find_executable
from app import builtins

cached_completions = []
error_in_completion = None


def complete(text, state):
    # This is a bizarre interface for readline.
    # Will be called with state = 0, 1, 2, ... until it returns None.
    if state:
        try:
            return cached_completions[state]
        except IndexError:
            return None

    try:
        line_buffer = readline.get_line_buffer()
        if " " in line_buffer:
            raise NotImplementedError("tab completion on args not supported")

        cached_completions[:] = list(find_executable(text))
        cached_completions.extend(f for f in dir(builtins) if f.startswith(text))

        return cached_completions[0] if cached_completions else None
    except Exception as e:
        global error_in_completion
        error_in_completion = e


def raise_for_completion_error():
    """Error during completion are always swallowed, so raise up errors again"""
    if error_in_completion:
        raise error_in_completion


def init_readline():
    """Initialize readline with custom settings."""

    # Set the completer function
    readline.set_completer(complete)

    # Set the delimiter characters
    readline.set_completer_delims(" \t\n;")

    # Tricky https://stackoverflow.com/a/8072282/771768
    # Check if using libedit or GNU Readline
    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind -e")
        readline.parse_and_bind("bind '\t' rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
