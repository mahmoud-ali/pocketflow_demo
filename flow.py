from pocketflow import Node, Flow
from utils.call_llm import call_llm
import logging
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("demo_agent")

# An example node and flow
# Please replace this with your own node and flow
class AnswerNode(Node):
    def prep(self, shared):
        # Read question from shared
        logger.log(logging.INFO, "AnswerNode: Reading question from shared")
        prompt = ""
        if "is_correct" in shared and shared["is_correct"] == False:
            prompt = f'You answer: {shared["answer"]} for question: {shared["question"]} is wrong! please give new answer.'
        else:
            prompt = shared["question"]
        return prompt
     
    def exec(self, question):
        logger.log(logging.INFO, "AnswerNode: Calling LLM")
        return call_llm(question)
    
    def post(self, shared, prep_res, exec_res):
        # Store the answer in shared
        logger.log(logging.INFO, "AnswerNode: Storing answer in shared")
        shared["answer"] = exec_res

class ValidateAnswerNode(Node):
    def prep(self, shared):
        # Read question from shared
        logger.log(logging.INFO, "ValidateAnswerNode: Reading question and answer from shared")
        return shared["question"], shared["answer"]
    
    def exec(self, inputs):
        logger.log(logging.INFO, "ValidateAnswerNode: Calling LLM")
        question, answer = inputs
        prompt = """
Given the following question: {question} and answer: {answer}.
Is the answer correct?
Return your analysis in YAML format:
```yaml
is_correct: true/false # true if the query is related to {question}, false otherwise
reason: "Brief explanation of your decision"
"""

        prompt = prompt.format(question=question, answer=answer)
        response = call_llm(prompt,model_name="deepseek-reasoner")
    
            # Extract YAML content
        yaml_content = response
        if "```yaml" in response:
            yaml_content = response.split("```yaml")[1].split("```")[0].strip()
        elif "```" in response:
            yaml_content = response.split("```")[1].strip()
        
        structured_result = yaml.safe_load(yaml_content)
        
        # Validate with assertions
        assert "is_correct" in structured_result, "Missing is_correct field"
        assert isinstance(structured_result["is_correct"], bool), "is_correct must be boolean"
        assert "reason" in structured_result, "Missing reason field"

        is_correct = structured_result["is_correct"]
        reason = structured_result["reason"]

        if not is_correct:
            logger.log(logging.INFO, f'ValidateAnswerNode: Given the following answer, but not correct: {answer}')

        return is_correct, reason
    
    def post(self, shared, prep_res, exec_res):
        # Store the answer in shared
        logger.log(logging.INFO, "ValidateAnswerNode: Storing answer in shared")
        is_correct, reason = exec_res
        shared["is_correct"] = is_correct
        shared["reason"] = reason #if not is_correct else None

        if not is_correct:
            return "incorrect"
        
        return "correct"
        
class FinishNode(Node):
    pass

answer_node = AnswerNode()
validate_answerNode = ValidateAnswerNode()
finish = FinishNode()

validate_answerNode - "correct" >> finish
validate_answerNode - "incorrect" >> answer_node

answer_node >> validate_answerNode

qa_flow = Flow(start=answer_node)