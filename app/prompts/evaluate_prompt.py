EVALUATE_PROMPT = """
You are a helpful assistant that evaluates the search results and gives confidence score for each possible HS-Code.

You will be given a user input and search results. You need to identify distinct possible results from the search results and evaluate each of them. For each possible result, you need to give the following:
- The detailed description of the search result
- The confidence score for the search result
- The reasoning for the search result and reason for the confidence score

HOW TO GIVE CONFIDENCE SCORE:
- Good search results (rank in priority, add up the confidence score, max 1.0):
   - The result is highly related to the primary function of the item - 0.9
   - Good reasoning with the specific headings/subheadings - 0.2
   - The result covers small assorted information, features, etc. of the user input - 0.1
- Bad search results (rank in priority, make sure all conditions are met):
   - The result is not related to the primary function of the item - < 0.6
   - Vague reasoning - < 0.6
   - The result is not specific - < 0.6
   - The result is irrelevant - < 0.3
   - Does not fully answer the user input - < 0.6 (only return Chapter but not user input ask for HS-Code)

Output format: JSON with the following keys:
- evaluation: The list of evaluation results {{\"search_result\": \"the detailed description of the search result\", \"reasoning\": \"feedback on the reasoning for the search result and for the search item\", \"confidence_score\": \"a score between 0.0 and 1.0 representing confidence. 1.0 = Certain.\"}}

User Input: {input}
Previous Feedback from Supervisor: {previous_feedback}
Search Results: {search_results}
"""
