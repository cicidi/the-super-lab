"""Mock MCP client for TST-Q. Calls the in-process mock server only."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from server import handle  # noqa: E402


def call(tool, args):
    return handle(tool, args)


if __name__ == "__main__":
    call("search", {"query": "iPhone purchase"})
    call("book", {"item": "iPhone", "mock": True})
