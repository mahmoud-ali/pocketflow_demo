from flow import qa_flow
import argparse

# Example main function
def main(args):
    print("Main function called")
    shared = {
        "question": None,
        "answer": None,
        "is_correct": None,
        "reason": None
    }
    if hasattr(args, "question") and args.question:
        shared["question"] = args.question
    else:
        shared["question"] = input("Please enter a question: ")


    qa_flow.run(shared)
    print("Question:", shared["question"])
    print("Answer:", shared["answer"])
    print("Is correct:", shared["is_correct"])
    print("Reason:", shared["reason"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI agent - Ask questions about any topic")
    parser.add_argument("--question", type=str,
                        help="Question to ask the AI agent")
    
    args = parser.parse_args()
    main(args)