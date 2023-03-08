from configparser import ConfigParser
import sys
import os
import subprocess
import logging
import whisper
import openai


class Assistant:
    def __init__(self, firstname) -> None:
        self.firstname = firstname
        self.model = None
        self.transscription = None

    def setup_assistant(self):
        config = ConfigParser()
        config.read('config.cfg')
        openai.api_key = config.get('auth', 'OPENAI_API_KEY')

    def load_speech_to_text_model(self, modelname):
        """For Whisper there are: 'tiny', 'base', 'small' models'"""
        self.model = whisper.load_model(modelname)
        
    def transcribe_audio_file(self, audiofilename):
        if self.model:
            self.transscription = self.model.transcribe(audiofilename, fp16=False)
        else:
            print('First load a speech_to_text_model')

    def response(self):
        if self.transscription:
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.transscription["text"],
            temperature=0.7,
            max_tokens=10,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        else:
            print('First transcribe the audiofile')
        return response["choices"][0]["text"][2:]

def main():
    logging.basicConfig(filename='interaction.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
    python_exec_path = sys.executable
    subprocess.run([python_exec_path, 'audio_realtimeplot.py'])

    print(pro_plot)

    howie = Assistant('Howie')
    howie.setup_assistant()
    howie.load_speech_to_text_model('base')
    howie.transcribe_audio_file("audio.wav")

    user_text = howie.transscription["text"]
    print(user_text)

    logging.info(f'From user to assistant: {user_text}')

    assistant_text = howie.response()
    print(assistant_text)

    logging.info(f'From user to assistant: {assistant_text}')

    os.remove('audio.wav')
    print("audio.wav has been deleted")

if __name__ == '__main__':
    main()