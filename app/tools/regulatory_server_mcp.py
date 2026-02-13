import logging
import sys
from pathlib import Path

# Allow running this file directly: ensure app is on path
_here = Path(__file__).resolve().parent
_app = _here.parent
if str(_app) not in sys.path:
    sys.path.insert(0, str(_app))

from fastmcp import FastMCP
from index_query import IndexQuery

mcp = FastMCP("Regulatory Auditor Server")


index_query = IndexQuery()


@mcp.tool()
def get_regulatory_rules(rule_number: str = "all") -> str:
    """
    Retrieves the General Interpretative Rules (GIR) from the STCCED 2022 PDF.
    Use this to resolve classification conflicts (e.g., composite goods).
    """
    query = f"What is the text of General Interpretative Rule {rule_number}?"
    if rule_number == "all":
        query = "List and explain all General Interpretative Rules (GIR) 1 through 6."

    # Calls your existing RAG logic
    return index_query.index_query(query=query)


@mcp.tool()
def search_stcced_pdf(query: str) -> str:
    """
    Performs a semantic search against the full STCCED 2022 knowledge base.
    Returns technical descriptions and HS-Code candidates.
    """
    return index_query.index_query(query=query)


if __name__ == "__main__":
    # Runs the server using stdio (Standard Input/Output)
    # This is the industry standard for local agent-server communication
    mcp.run()
