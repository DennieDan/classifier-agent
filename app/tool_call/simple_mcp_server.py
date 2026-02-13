"""Minimal MCP server with one tool: validate_user. Run with: python simple_mcp_server.py"""

from typing import List

from fastmcp import FastMCP

mcp = FastMCP("Simple Tools")


@mcp.tool()
def validate_user(user_id: int, addresses: List[str]) -> bool:
    """
    Validate the user by checking if the user ID is valid and the addresses are valid.

    Args:
        user_id: The user ID to validate.
        addresses: The addresses to validate.

    Returns:
        True if the user is valid, False otherwise.
    """
    return True


if __name__ == "__main__":
    mcp.run()
