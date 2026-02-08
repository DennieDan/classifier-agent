"""Console interface for the classifier agent."""

from agent import app


def get_input_from_console() -> str:
    """Get user input from the console."""
    return input("Enter text to classify: ").strip()


def run_classifier(user_input: str) -> dict:
    """Run the classifier agent on the given input."""
    inputs = {
        "user_input": user_input,
        "classification": "",
        "confidence": 0.0,
        "thought_process": "",
        "next_step": "",
    }
    return app.invoke(inputs)


def main():
    """Interactive console loop: get input, classify, display result."""
    print("Classifier Agent - Console Mode")
    print("Type your input and press Enter. Type 'quit' or 'exit' to stop.\n")

    while True:
        user_input = get_input_from_console()

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if not user_input:
            print("Please enter some text.\n")
            continue

        result = run_classifier(user_input)
        print(f"\nThought process: {result['thought_process']}")
        print(
            f"Classification: {result['classification']} "
            f"(Confidence: {result['confidence']:.2f})\n"
        )


if __name__ == "__main__":
    main()
