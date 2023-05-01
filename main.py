#!/usr/bin/env python3

"""
This is a Python-based interface for interacting with the OpenAI GPT-3
assistant API using audio input from a microphone. It's a fun project that
I've been working on to explore the capabilities of the OpenAI API and
experiment with voice input.
"""

import os
import logging_config
import configparser
from assistant import Assistant
from transcription import TranscriptionHandler
from audio_recording import Recorder
from playsound import playsound
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav


def main():
    # Load configuration from file
    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'config.ini')
    config.read(config_file)

    # Set the logging level and if the logs should go to console
    to_console = config.getboolean('general', 'TO_CONSOLE')
    log_level = config.get('general', 'LOG_LEVEL')
    logging_config.configure_logging(log_level, to_console)

    # Would you like to keep the recorded audio file?
    delete_audio = config.getboolean('general', 'DELETE_AUDIO')

    # Give your assistant a name!
    name = config.get('general', 'ASSISTANT_NAME')
    howie = Assistant(name)
    # howie.setup_assistant()

    # This will record your voice with the default input device of your machine
    mic_recorder = Recorder()
    mic_recorder.record(max_duration=10)

    # Whisper tries to transcribe your recorded audio. All locally.
    model = config.get('general', 'MODEL')
    transcript = TranscriptionHandler()
    transcript.load_speech_to_text_model(model)
    transcript.transcribe_audio_file(
        mic_recorder.filename, delete=delete_audio)
    user_text = transcript.transcription["text"]

    # The transcripted text is beeing sent to openAI
    assistant_text = howie.response(from_user=user_text)

    # Print or log conversation
    if not to_console:
        print(f"From user to assistant:{user_text}")
        if assistant_text:
            print(f"From assistant to user: {assistant_text}")
        else:
            print(f"Upsi. No response from {name}")

    # Play Audio of the response
    # generate audio from text
    text_prompt = assistant_text
    audio_array = generate_audio(text_prompt)

    # save audio to disk
    write_wav("audio.wav", SAMPLE_RATE, audio_array)
    playsound('audio.mp3')


if __name__ == '__main__':
    main()
