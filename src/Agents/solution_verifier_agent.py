##################### Solution Verifier #########################
from .conversable_agent import MyConversableAgent
from src.Models.llm_config import gpt3_config

class SolutionVerifierAgent(MyConversableAgent):
    description = """
                        After the Student answers, you check the Students's solutions to math problems. 
                        You interact with the Tutor not the Student. 
                        After the Student answers, you ask the Programmer to generate code to check and visualize the solution.
                    """
    def __init__(self):
        super().__init__(
                name="SolutionVerifier",
                human_input_mode="NEVER",
                llm_config=gpt3_config,
                system_message=self.description,
                description=self.description
            )