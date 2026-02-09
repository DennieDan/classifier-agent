SEARCH_PROMPT = """Search for the HS-Code of: {search_item}

Return the HS-Code (Harmonized System Code) and any relevant classification details."""

RECURSIVE_SEARCH_PROMPT = """The previous search for "{search_item}" did not yield a confident result.

**Search recursively** using the following guidance:
{feedback}

Try: broader terms, synonyms, related product categories, or alternative phrasings.
Return the best HS-Code match you can find with supporting details."""
