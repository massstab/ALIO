import whisper
import os
import logging


class TranscriptionHandler:
    def __init__(self) -> None:
        pass

    def load_speech_to_text_model(self, modelname):
        """For Whisper there are: 'tiny', 'base', 'small' models'"""
        self.model = whisper.load_model(modelname)

    def transcribe_audio_file(self, filename, delete=True):
        if self.model:
            self.transcription = self.model.transcribe(filename, fp16=False)
            if delete:
                os.remove(filename)
            logging.info(f"Temporary audiofile {filename} has been deleted")
        else:
            print('First load a speech_to_text_model')
