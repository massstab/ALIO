#!/usr/bin/env python3

"""
This is a Python-based interface for interacting with the OpenAI GPT-3
assistant API using audio input from a microphone. It's a fun project that
I've been working on to explore the capabilities of the OpenAI API and
experiment with voice input.
"""

import logging_config
from assistant import Assistant
from transcription import TranscriptionHandler
from audio_recording import Recorder


def main():
    # Set the logging level and if the logs should go to console
    to_console = True
    log_level = "INFO"
    logging_config.configure_logging(log_level, to_console)

    # Would you like to keep the recorded audio file?
    delete_audio = False

    # Give your assistant a name!
    name = 'Howie'
    howie = Assistant(name)
    howie.setup_assistant()

    # This will record your voice with the default input device of your machine
    mic_recorder = Recorder()
    mic_recorder.record(max_duration=10)

    # Whisper tries to transcribe your recorded audio. All locally.
    transcript = TranscriptionHandler()
    transcript.load_speech_to_text_model('base')
    transcript.transcribe_audio_file(mic_recorder.filename, delete=delete_audio)
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


if __name__ == '__main__':
    main()
