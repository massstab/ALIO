import logging
from configparser import ConfigParser
import openai
from hugchat import hugchat


class Assistant:
    """
    This class represents the assistant with methods that handels the workflow
    from asking the assistant (a user_text) to the response (assistant_text)
    """

    def __init__(self, firstname) -> None:
        self.firstname = firstname
        self.usertext = ''

    def setup_assistant_openai(self):
        config = ConfigParser()
        try:
            config.read('config.ini')
            openai.api_key = config.get('auth', 'OPENAI_API_KEY')
        except FileNotFoundError as e:
            logging.error(f"Config file not found: {e}")

        except KeyError as e:
            logging.error(f"Missing API key in config file: {e}")

    def get_usertext(self, userinput):
        self.usertext = userinput
        logging.info(f'From user to assistant: {userinput}')

    def response_openai(self, from_user):
        self.get_usertext(from_user)
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.usertext,
                temperature=0.7,
                max_tokens=50,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0)
            response_text = response["choices"][0]["text"][2:]  # type: ignore
            logging.info(f'From assistant to user: {response_text}')
            return response_text

        except openai.error.AuthenticationError as e:  # type: ignore
            # Handle authentication error, e.g. check credentials or log
            print(f"OpenAI API request was not authorized: {e}")
            return None

    def response_hugging_chat(self, from_user):
        self.get_usertext(from_user)
        chatbot = hugchat.ChatBot()
        # id = chatbot.new_conversation()
        # print("id: ", id)
        # chatbot.change_conversation(id)
        response_text = chatbot.chat(self.usertext)
        logging.info(f'From assistant to user: {response_text}')
        chatbot.get_conversation_list()
        return response_text
