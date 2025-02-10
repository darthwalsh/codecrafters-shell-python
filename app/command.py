from contextlib import contextmanager
from dataclasses import dataclass, replace
import os
import re
from typing import Self


@dataclass(frozen=True)
class Redirect:
    fd: int
    file: str  # empty means check next arg
    output: bool
    append: bool

    @staticmethod
    def parse(token: str) -> Self | None:
        match = re.match(r"(\d+)*(>>?|<)(.*)", token)
        if not match:
            return None

        fd, op, file = match.groups()
        if not fd:
            fd = 0 if op == "<" else 1

        return Redirect(int(fd), file, op != "<", op == ">>")


@dataclass(frozen=True)
class Command:
    command: str
    args: tuple[str]
    redirects: tuple[Redirect] = ()

    @contextmanager
    def redirect(self):
        """Redirects the command's output to the specified files"""
        fds = []
        for redirect in self.redirects:
            if not redirect.output:
                raise NotImplementedError("input redirection not supported")

            copy = os.dup(redirect.fd)

            new_file = open(redirect.file, "a" if redirect.append else "w")
            os.dup2(new_file.fileno(), redirect.fd)

            fds.append((new_file, copy, redirect.fd))

        try:
            yield
        finally:
            for new_file, copy, fd in reversed(fds):
                os.dup2(copy, fd)
                os.close(copy)
                new_file.close()

    @staticmethod
    def parse(tokens: list[str]) -> "Command":
        """Takes a list of expanded tokens and parses the redirection ops"""
        command_args = []
        redirects = []
        it = iter(tokens)
        for token in it:
            redirect = Redirect.parse(token)
            if redirect:
                if not redirect.file:
                    try:
                        file = next(it)
                    except StopIteration:
                        raise ValueError("unexpected end of command")
                    redirect = replace(redirect, file=file)
                redirects.append(redirect)
            else:
                command_args.append(token)
        return Command(command_args[0], tuple(command_args[1:]), tuple(redirects))
