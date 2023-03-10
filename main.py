from configparser import ConfigParser
import sys
import os
import subprocess
import logging
import whisper
import openai

from audio_recording import Recorder


class Assistant:
    """
    This class represents the assistant with methods that handels the workflow
    from asking the assistant (a user_text) to the response (assistant_text)
    """

    def __init__(self, firstname) -> None:
        self.firstname = firstname
        self.usertext = None

    def setup_assistant(self):
        config = ConfigParser()
        config.read('config.cfg')
        openai.api_key = config.get('auth', 'OPENAI_API_KEY')

    def get_usertext(self, userinput):
        self.usertext = userinput

    def response(self):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.usertext,
            temperature=0.7,
            max_tokens=5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response["choices"][0]["text"][2:]  # type: ignore


class TranscriptionHandler:
    def __init__(self) -> None:
        pass

    def load_speech_to_text_model(self, modelname):
        """For Whisper there are: 'tiny', 'base', 'small' models'"""
        self.model = whisper.load_model(modelname)

    def transcribe_audio_file(self, filename):
        if self.model:
            self.transcription = self.model.transcribe(filename, fp16=False)
            os.remove(filename)
            logging.info(f"Temporary audiofile {filename} has been deleted")
        else:
            print('First load a speech_to_text_model')


def main():

    logging.basicConfig(filename='interaction.log', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    howie = Assistant('Howie')
    howie.setup_assistant()

    mic_recorder = Recorder()
    mic_recorder.record()

    transcript = TranscriptionHandler()
    transcript.load_speech_to_text_model('base')
    transcript.transcribe_audio_file(mic_recorder.filename)

    user_text = transcript.transcription["text"]
    howie.get_usertext(user_text)
    logging.info(f'From user to assistant: {user_text}')

    assistant_text = howie.response()

    logging.info(f'From assistant to user: {assistant_text}')


if __name__ == '__main__':
    main()
