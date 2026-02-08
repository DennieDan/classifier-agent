CLASSIFIER_PROMPT = """
You are a helpful assistant that classifies items into categories.

You will be given a item which is a sentence containing word(s) related to food or drink and you need to classify them into the following categories:
- FOOD
- DRINK
- BOTH
- OTHERS

Return the classification and the confidence score for the classification.

Input: {item}

Output format: JSON with the following keys:
- result: The classification of the item (FOOD, DRINK, OTHERS)
- conf: The confidence score for the classification (0.0 to 1.0)

Example:
{{ "result": "FOOD", "conf": 0.95 }}

"I want to eat KFC"
Output: {{ "result": "FOOD", "conf": 0.5 }}

"There are 3 cups of bubble tea in the fridge."
Output: {{ "result": "DRINK", "conf": 0.8 }}

"I want to eat a burger and drink a coke."
Output: {{ "result": "BOTH", "conf": 0.95 }}

"This nasi lemak makes me puke."
Output: {{ "result": "FOOD", "conf": 0.70 }}

"This coke is too sweet."
Output: {{ "result": "DRINK", "conf": 0.9 }}
"""
