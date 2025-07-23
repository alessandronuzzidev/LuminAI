from controller.abstract_controller import AbstractController


class ControllerCLI(AbstractController):
    def __init__(self):
        super().__init__()

    def send_message_to_llm(self, message):
        # Implementation for sending a message to the LLM
        pass

    def receive_message_from_llm(self, response):
        # Implementation for receiving a message from the LLM
        pass

    def update_configuration(self, config):
        # Implementation for updating configuration
        pass