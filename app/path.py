from pathlib import Path
import os


def find_executable(prefix):
    for path in os.environ["PATH"].split(":"):
        path = Path(path)
        if not path.is_dir():
            continue
        for f in path.iterdir():
            # Don't check f.is_file() because that raises if the link
            # points to directory we can't access
            if not os.path.islink(f) and not os.path.isfile(f):
                continue
            is_executable = os.access(f, os.X_OK)
            if is_executable and f.name.startswith(prefix):
                yield f.name



def resolve(command) -> str | None:
    for path in os.environ["PATH"].split(":"):
        path = Path(path) / command
        if path.exists():
            return path
