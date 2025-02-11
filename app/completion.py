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

        commands = set(find_executable(text)) | {f for f in dir(builtins) if f.startswith(text)}
        if len(commands) == 1:
            commands = [c + " " for c in commands]
        cached_completions[:] = commands

        return cached_completions[0] if cached_completions else None
    except Exception as e:
        global error_in_completion
        error_in_completion = e


def match_display_hook(_substitution, matches, _longest_match_length):
    try:
        print()
        print(*matches, sep="  ")
        print(PROMPT + readline.get_line_buffer(), end="")
    except Exception as e:
        global error_in_completion
        error_in_completion = e


def raise_for_completion_error():
    """Error during completion are always swallowed, so raise up errors again"""
    if error_in_completion:
        raise error_in_completion


def init_readline(prompt):
    """Initialize readline with custom settings."""
    global PROMPT
    PROMPT = prompt

    readline.set_completer(complete)
    readline.set_completion_display_matches_hook(match_display_hook)

    readline.set_completer_delims(" \t\n;")

    # Tricky https://stackoverflow.com/a/8072282/771768
    # Check if using libedit or GNU Readline
    if "libedit" in readline.__doc__:
        # Warning: libedit does not support some GNU readline features
        # https://pewpewthespells.com/blog/osx_readline.html
        # readline.parse_and_bind("bind -e")
        # readline.parse_and_bind("bind '\t' rl_complete")
        raise RuntimeError("libedit readline not supported, use GNU readline")
    else:
        readline.parse_and_bind("tab: complete")
