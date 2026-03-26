import sys
from pathlib import Path

# Allow running this file directly: ensure app is on path
_here = Path(__file__).resolve().parent
_app = _here.parent
if str(_app) not in sys.path:
    sys.path.insert(0, str(_app))

from index_query import IndexQuery

_index_query: IndexQuery | None = None


def _get_index_query() -> IndexQuery:
    """Lazy init so import (and uvicorn bind) is not blocked by HF embed + Chroma load."""
    global _index_query
    if _index_query is None:
        _index_query = IndexQuery()
    return _index_query


def get_regulatory_rules(rule_number: str = "all") -> str:
    """
    Retrieves the General Interpretative Rules (GIR) from the STCCED 2022 PDF.
    Use this to resolve classification conflicts (e.g., composite goods).
    """
    query = f"What is the text of General Interpretative Rule {rule_number}?"
    if rule_number == "all":
        query = "List and explain all General Interpretative Rules (GIR) 1 through 6."

    # Calls your existing RAG logic
    return _get_index_query().index_query(query=query)


def search_stcced_pdf(query: str) -> str:
    """
    Performs a semantic search against the full STCCED 2022 knowledge base.
    Returns technical descriptions and HS-Code candidates.

    Args:
        query: The query to search the STCCED 2022 knowledge base. Give as specific query as possible.
        E.g. "Which chapters/Headings does the item '...' fall in? Give description of the Chapters/Headings."

    Returns:
        The search results.
    """
    return _get_index_query().index_query(query=query)
