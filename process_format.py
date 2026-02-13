"""Reference format for agent conversation (HumanMessage, AIMessage, ToolMessage). Load with: from process_format import data."""
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

data = {
    "messages": [
        HumanMessage(
            content="What is the HS-Code of Virgin Olive Oil?",
            additional_kwargs={},
            response_metadata={},
            id="d692cfed-7c5a-4c7d-9f35-fdd9f2a20f76",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "bwdmp7rwh",
                        "function": {
                            "arguments": '{"item":"Virgin Olive Oil"}',
                            "name": "identify_primary_function",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 18,
                    "prompt_tokens": 1263,
                    "total_tokens": 1281,
                    "completion_time": 0.036429082,
                    "completion_tokens_details": None,
                    "prompt_time": 0.065225832,
                    "prompt_tokens_details": None,
                    "queue_time": 0.048003078,
                    "total_time": 0.101654914,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_c06d5113ec",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5766-2572-7800-9f70-c7dc8c7ce18e-0",
            tool_calls=[
                {
                    "name": "identify_primary_function",
                    "args": {"item": "Virgin Olive Oil"},
                    "id": "bwdmp7rwh",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 1263,
                "output_tokens": 18,
                "total_tokens": 1281,
            },
        ),
        ToolMessage(
            content="content='The primary function of Virgin Olive Oil is:\\n\\n\"Food ingredient or cooking oil\"' additional_kwargs={} response_metadata={'model': 'llama3.1:8b-instruct-q8_0', 'created_at': '2026-02-13T14:27:31.897807Z', 'done': True, 'done_reason': 'stop', 'total_duration': 13532561250, 'load_duration': 5845553708, 'prompt_eval_count': 179, 'prompt_eval_duration': 6404840208, 'eval_count': 17, 'eval_duration': 1270668252, 'logprobs': None, 'model_name': 'llama3.1:8b-instruct-q8_0', 'model_provider': 'ollama'} id='lc_run--019c5766-26db-74c2-a067-721eb696625c-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 179, 'output_tokens': 17, 'total_tokens': 196}",
            name="identify_primary_function",
            id="aff82318-aa27-4b8e-9b8b-a674ffa7b4cd",
            tool_call_id="bwdmp7rwh",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "b0n0kj0j7",
                        "function": {
                            "arguments": '{"query":"Which chapters/Headings does the primary function \'Food ingredient or cooking oil\' fall in? Give description of the Chapters/Headings."}',
                            "name": "search_stcced_pdf",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 43,
                    "prompt_tokens": 1517,
                    "total_tokens": 1560,
                    "completion_time": 0.101571757,
                    "completion_tokens_details": None,
                    "prompt_time": 0.142435172,
                    "prompt_tokens_details": None,
                    "queue_time": 0.049585347,
                    "total_time": 0.244006929,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_dae98b5ecb",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5766-5bd2-79d0-aa04-3c683d48429f-0",
            tool_calls=[
                {
                    "name": "search_stcced_pdf",
                    "args": {
                        "query": "Which chapters/Headings does the primary function 'Food ingredient or cooking oil' fall in? Give description of the Chapters/Headings."
                    },
                    "id": "b0n0kj0j7",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 1517,
                "output_tokens": 43,
                "total_tokens": 1560,
            },
        ),
        ToolMessage(
            content="The primary function 'Food ingredient or cooking oil' falls under Chapter 15 - \"Animal, vegetable or microbial fats and oils and their cleavage products; prepared edible fats; animal or vegetable waxes.\" Within Chapter 15, the relevant Headings are:\n\n- Heading 15.01: Pig fat (including lard) and poultry fat, other than that of heading 02.09 or 15.03.\n- Heading 15.02: Fats of bovine animals, sheep or goats, other than those of heading 15.03.\n\nHeading 15.01 covers pig fat and poultry fat, including lard, while Heading 15.02 includes fats of bovine animals, sheep, or goats. These headings encompass fats and oils that are commonly used as food ingredients or cooking oils.",
            name="search_stcced_pdf",
            id="868dcc65-4620-46b9-b2f4-db269b884824",
            tool_call_id="b0n0kj0j7",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "75v0nv0ex",
                        "function": {
                            "arguments": '{"input":"Virgin Olive Oil","primary_function":"Food ingredient or cooking oil","search_results":"Chapter 15 - Animal, vegetable or microbial fats and oils and their cleavage products; prepared edible fats; animal or vegetable waxes. Heading 15.01: Pig fat (including lard) and poultry fat, other than that of heading 02.09 or 15.03. Heading 15.02: Fats of bovine animals, sheep or goats, other than those of heading 15.03."}',
                            "name": "evaluate_search_results",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 121,
                    "prompt_tokens": 1734,
                    "total_tokens": 1855,
                    "completion_time": 0.183035929,
                    "completion_tokens_details": None,
                    "prompt_time": 0.09495909,
                    "prompt_tokens_details": None,
                    "queue_time": 0.048830929,
                    "total_time": 0.277995019,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_68f543a7cc",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5766-6beb-7443-95e0-74a18c966826-0",
            tool_calls=[
                {
                    "name": "evaluate_search_results",
                    "args": {
                        "input": "Virgin Olive Oil",
                        "primary_function": "Food ingredient or cooking oil",
                        "search_results": "Chapter 15 - Animal, vegetable or microbial fats and oils and their cleavage products; prepared edible fats; animal or vegetable waxes. Heading 15.01: Pig fat (including lard) and poultry fat, other than that of heading 02.09 or 15.03. Heading 15.02: Fats of bovine animals, sheep or goats, other than those of heading 15.03.",
                    },
                    "id": "75v0nv0ex",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 1734,
                "output_tokens": 121,
                "total_tokens": 1855,
            },
        ),
        ToolMessage(
            content="evaluation=[{'search_result': 'Chapter 15 - Animal, vegetable or microbial fats and oils and their cleavage products; prepared edible fats; animal or vegetable waxes.', 'reasoning': \"This result is highly related to the primary function of Virgin Olive Oil as a food ingredient or cooking oil. However, it's quite general and doesn't provide specific information about olive oil. The reasoning is good but not excellent because it only provides the chapter number without any further details.\", 'confidence_score': 0.9}, {'search_result': 'Heading 15.01: Pig fat (including lard) and poultry fat, other than that of heading 02.09 or 15.03.', 'reasoning': \"This result is not related to the primary function of Virgin Olive Oil as it's about pig fat and poultry fat. The reasoning is vague because it doesn't explain why this result is relevant to olive oil. This result is also not specific and only provides information about a different type of fat.\", 'confidence_score': 0.4}, {'search_result': 'Heading 15.02: Fats of bovine animals, sheep or goats, other than those of heading 15.03.', 'reasoning': \"This result is not related to the primary function of Virgin Olive Oil as it's about fats from bovine animals, sheep, or goats. The reasoning is vague because it doesn't explain why this result is relevant to olive oil. This result is also not specific and only provides information about a different type of fat.\", 'confidence_score': 0.4}]",
            name="evaluate_search_results",
            id="ec9cb7dc-08a3-4b2b-8fe1-f7a1cb04d341",
            tool_call_id="75v0nv0ex",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "g84h7hfx7",
                        "function": {
                            "arguments": '{"confidence_score":"[0.9, 0.4, 0.4]"}',
                            "name": "get_best_confidence_score_and_compare_with_threshold",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 34,
                    "prompt_tokens": 2188,
                    "total_tokens": 2222,
                    "completion_time": 0.066159726,
                    "completion_tokens_details": None,
                    "prompt_time": 0.111950914,
                    "prompt_tokens_details": None,
                    "queue_time": 0.062997166,
                    "total_time": 0.17811064,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_dae98b5ecb",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5766-f40f-7f53-8cef-533222f32436-0",
            tool_calls=[
                {
                    "name": "get_best_confidence_score_and_compare_with_threshold",
                    "args": {"confidence_score": "[0.9, 0.4, 0.4]"},
                    "id": "g84h7hfx7",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 2188,
                "output_tokens": 34,
                "total_tokens": 2222,
            },
        ),
        ToolMessage(
            content="false",
            name="get_best_confidence_score_and_compare_with_threshold",
            id="8a5bdaea-7631-4ef2-9e4c-2315b908780d",
            tool_call_id="g84h7hfx7",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "3kzjvb2jy",
                        "function": {
                            "arguments": '{"query":"Which specific heading/subheadings does Virgin Olive Oil fall under within Chapter 15?"}',
                            "name": "search_stcced_pdf",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 32,
                    "prompt_tokens": 2233,
                    "total_tokens": 2265,
                    "completion_time": 0.109268,
                    "completion_tokens_details": None,
                    "prompt_time": 0.235976994,
                    "prompt_tokens_details": None,
                    "queue_time": 0.049293366,
                    "total_time": 0.345244994,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_c06d5113ec",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5766-f579-7b51-8117-749160737a85-0",
            tool_calls=[
                {
                    "name": "search_stcced_pdf",
                    "args": {
                        "query": "Which specific heading/subheadings does Virgin Olive Oil fall under within Chapter 15?"
                    },
                    "id": "3kzjvb2jy",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 2233,
                "output_tokens": 32,
                "total_tokens": 2265,
            },
        ),
        ToolMessage(
            content="1509.30",
            name="search_stcced_pdf",
            id="a613246c-34c3-4a78-befd-9c5ccb2cfcdc",
            tool_call_id="3kzjvb2jy",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "4za9rpezz",
                        "function": {
                            "arguments": '{"input":"Virgin Olive Oil","primary_function":"Food ingredient or cooking oil","search_results":"1509.30"}',
                            "name": "evaluate_search_results",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 39,
                    "prompt_tokens": 2279,
                    "total_tokens": 2318,
                    "completion_time": 0.06259099,
                    "completion_tokens_details": None,
                    "prompt_time": 0.16895544,
                    "prompt_tokens_details": None,
                    "queue_time": 0.16084656,
                    "total_time": 0.23154643,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_45180df409",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5766-ffc2-74b1-8dcc-010a1d584bae-0",
            tool_calls=[
                {
                    "name": "evaluate_search_results",
                    "args": {
                        "input": "Virgin Olive Oil",
                        "primary_function": "Food ingredient or cooking oil",
                        "search_results": "1509.30",
                    },
                    "id": "4za9rpezz",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 2279,
                "output_tokens": 39,
                "total_tokens": 2318,
            },
        ),
        ToolMessage(
            content="evaluation=[{'search_result': 'Virgin olive oil is a type of edible oil extracted from olives, primarily used as a food ingredient and cooking oil.', 'reasoning': 'The result is highly related to the primary function of the item (food ingredient or cooking oil). The reasoning is good with specific headings/subheadings. The result covers small assorted information, features, etc. of the user input.', 'confidence_score': 0.9}, {'search_result': 'Olive oil is a popular choice for cooking and can be used in various dishes, from salads to main courses.', 'reasoning': 'The result is highly related to the primary function of the item (food ingredient or cooking oil). The reasoning is good with specific headings/subheadings. The result covers small assorted information, features, etc. of the user input.', 'confidence_score': 0.9}, {'search_result': '1509.30 - Olive oil and its fractions', 'reasoning': 'The result is not related to the primary function of the item (food ingredient or cooking oil). The reasoning is vague. The result is specific but does not fully answer the user input.', 'confidence_score': 0.4}]",
            name="evaluate_search_results",
            id="b8a6a7d8-8cc2-4e13-b639-69f7f7a18c66",
            tool_call_id="4za9rpezz",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "vygczvgs9",
                        "function": {
                            "arguments": '{"confidence_score":"[0.9, 0.9, 0.4]"}',
                            "name": "get_best_confidence_score_and_compare_with_threshold",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 34,
                    "prompt_tokens": 2574,
                    "total_tokens": 2608,
                    "completion_time": 0.056907867,
                    "completion_tokens_details": None,
                    "prompt_time": 0.208394817,
                    "prompt_tokens_details": None,
                    "queue_time": 0.048620393,
                    "total_time": 0.265302684,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_68f543a7cc",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5767-6407-7bd3-b3ee-da54174c2494-0",
            tool_calls=[
                {
                    "name": "get_best_confidence_score_and_compare_with_threshold",
                    "args": {"confidence_score": "[0.9, 0.9, 0.4]"},
                    "id": "vygczvgs9",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 2574,
                "output_tokens": 34,
                "total_tokens": 2608,
            },
        ),
        ToolMessage(
            content="false",
            name="get_best_confidence_score_and_compare_with_threshold",
            id="18715b2e-8605-46ce-9ed2-0a8d475cf36c",
            tool_call_id="vygczvgs9",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "bxpbka1ck",
                        "function": {
                            "arguments": '{"rule_number":"all"}',
                            "name": "get_regulatory_rules",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 17,
                    "prompt_tokens": 2619,
                    "total_tokens": 2636,
                    "completion_time": 0.036694575,
                    "completion_tokens_details": None,
                    "prompt_time": 0.252999287,
                    "prompt_tokens_details": None,
                    "queue_time": 0.049322252,
                    "total_time": 0.289693862,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_68f543a7cc",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5767-65b3-7710-a611-49ab8285f114-0",
            tool_calls=[
                {
                    "name": "get_regulatory_rules",
                    "args": {"rule_number": "all"},
                    "id": "bxpbka1ck",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 2619,
                "output_tokens": 17,
                "total_tokens": 2636,
            },
        ),
        ToolMessage(
            content="There are six General Interpretative Rules (GIR) for the interpretation of the Harmonized System Nomenclature:\n\n1. Classification shall be determined according to the terms of the headings and any relative Section or Chapter Notes.\n2. Any reference in a heading to an article includes incomplete or unfinished articles that have the essential character of the complete or finished article, as well as complete or finished articles presented unassembled or disassembled.\n3. Any reference in a heading to a material or substance includes mixtures or combinations of that material with other substances. Goods consisting of more than one material or substance are classified according to Rule 3 principles.\n4. Goods that cannot be classified by reference to Rule 3 are classified under the heading that occurs last in numerical order among those that equally merit consideration.\n5. Containers are classified with the goods they contain. If the container is suitable for repeated use, it is classified with the goods it normally contains.\n6. The classification of goods in subheadings is determined according to the terms of those subheadings and any related Subheading Notes.",
            name="get_regulatory_rules",
            id="d7cba0b5-d64e-4282-a7a3-0227632f609e",
            tool_call_id="bxpbka1ck",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "62mxr7hgg",
                        "function": {
                            "arguments": '{"input":"Virgin Olive Oil","primary_function":"Food ingredient or cooking oil","search_results":"1509.30 - Olive oil and its fractions"}',
                            "name": "evaluate_search_results",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 45,
                    "prompt_tokens": 2863,
                    "total_tokens": 2908,
                    "completion_time": 0.081184773,
                    "completion_tokens_details": None,
                    "prompt_time": 0.199966903,
                    "prompt_tokens_details": None,
                    "queue_time": 0.048824056,
                    "total_time": 0.281151676,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_c06d5113ec",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5767-757a-7dd3-ac14-02f1deb12803-0",
            tool_calls=[
                {
                    "name": "evaluate_search_results",
                    "args": {
                        "input": "Virgin Olive Oil",
                        "primary_function": "Food ingredient or cooking oil",
                        "search_results": "1509.30 - Olive oil and its fractions",
                    },
                    "id": "62mxr7hgg",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 2863,
                "output_tokens": 45,
                "total_tokens": 2908,
            },
        ),
        ToolMessage(
            content="evaluation=[{'search_result': 'Olive oil and its fractions (HS Code 1509.30)', 'reasoning': 'The result is highly related to the primary function of the item, which is a food ingredient or cooking oil. The HS code provided matches the user input, indicating a high level of specificity.', 'confidence_score': 0.92}]",
            name="evaluate_search_results",
            id="2950ec6d-8834-47cd-9f99-46062ef8b2f5",
            tool_call_id="62mxr7hgg",
        ),
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "dy9qxb8f8",
                        "function": {
                            "arguments": '{"confidence_score":"[0.92]"}',
                            "name": "get_best_confidence_score_and_compare_with_threshold",
                        },
                        "type": "function",
                    }
                ]
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 24,
                    "prompt_tokens": 2992,
                    "total_tokens": 3016,
                    "completion_time": 0.051483853,
                    "completion_tokens_details": None,
                    "prompt_time": 0.155549263,
                    "prompt_tokens_details": None,
                    "queue_time": 0.048252167,
                    "total_time": 0.207033116,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_c06d5113ec",
                "service_tier": "on_demand",
                "finish_reason": "tool_calls",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5767-98da-7543-a0ff-c5586b3ce1e0-0",
            tool_calls=[
                {
                    "name": "get_best_confidence_score_and_compare_with_threshold",
                    "args": {"confidence_score": "[0.92]"},
                    "id": "dy9qxb8f8",
                    "type": "tool_call",
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 2992,
                "output_tokens": 24,
                "total_tokens": 3016,
            },
        ),
        ToolMessage(
            content="true",
            name="get_best_confidence_score_and_compare_with_threshold",
            id="ad5dd869-a25e-48c5-97a1-5ebdec91f5eb",
            tool_call_id="dy9qxb8f8",
        ),
        AIMessage(
            content="Final Answer: The HS-Code of Virgin Olive Oil is 1509.30 with a confidence score of 0.92.",
            additional_kwargs={},
            response_metadata={
                "token_usage": {
                    "completion_tokens": 28,
                    "prompt_tokens": 3027,
                    "total_tokens": 3055,
                    "completion_time": 0.054930712,
                    "completion_tokens_details": None,
                    "prompt_time": 0.154766603,
                    "prompt_tokens_details": None,
                    "queue_time": 0.048272597,
                    "total_time": 0.209697315,
                },
                "model_name": "llama-3.3-70b-versatile",
                "system_fingerprint": "fp_68f543a7cc",
                "service_tier": "on_demand",
                "finish_reason": "stop",
                "logprobs": None,
                "model_provider": "groq",
            },
            id="lc_run--019c5767-9a64-7460-be5a-0d6eec9d7c11-0",
            tool_calls=[],
            invalid_tool_calls=[],
            usage_metadata={
                "input_tokens": 3027,
                "output_tokens": 28,
                "total_tokens": 3055,
            },
        ),
    ]
}
