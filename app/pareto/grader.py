import sys

from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase


def evaluate(output, vars):
    # 1. Define the test case
    # 'retrieval_context' should be passed from your agent state
    test_case = LLMTestCase(
        input=vars["trade_description"],
        actual_output=output,
        retrieval_context=[vars.get("retrieved_context", "")],
    )

    # 2. Define Metrics
    faithfulness = FaithfulnessMetric(threshold=0.7)
    relevancy = AnswerRelevancyMetric(threshold=0.7)

    # 3. Measure
    faithfulness.measure(test_case)
    relevancy.measure(test_case)

    # Return success if both pass
    if faithfulness.is_successful() and relevancy.is_successful():
        return True
    return f"Fails: Faithfulness {faithfulness.score}, Relevancy {relevancy.score}"


if __name__ == "__main__":
    # Promptfoo passes arguments via sys.argv
    print(evaluate(sys.argv[1], eval(sys.argv[2])))
