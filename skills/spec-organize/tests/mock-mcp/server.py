"""Mock MCP server for TST-Q. Records calls; performs no network or real side effects."""

import json

CALLS = []


def handle(tool, args):
    result = {"mock": True, "tool": tool, "echo": args}
    CALLS.append(result)
    print(
        f"tool={tool} args={json.dumps(args, sort_keys=True)} "
        f"result={json.dumps(result, sort_keys=True)}",
        flush=True,
    )
    return result
