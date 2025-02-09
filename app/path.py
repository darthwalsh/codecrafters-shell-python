from pathlib import Path
import os


def resolve(command) -> str | None:
    for path in os.environ["PATH"].split(":"):
        path = Path(path) / command
        if path.exists():
            return path
