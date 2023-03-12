import logging_config
from assistant import Assistant
from transcription import TranscriptionHandler
from audio_recording import Recorder


def main():
    # Set the loggin level and if the logs should go to console
    to_console = True
    log_level = "INFO"
    logging_config.configure_logging(log_level, to_console)

    # Give your assistant a name!
    howie = Assistant('Howie')
    howie.setup_assistant()

    # This will record your voice with the default input device of your machine
    mic_recorder = Recorder()
    mic_recorder.record()

    # Whisper tries to transcript your recorded audio. All locally.
    transcript = TranscriptionHandler()
    transcript.load_speech_to_text_model('base')
    transcript.transcribe_audio_file(mic_recorder.filename)

    # The transcripted text is beeing sent to openAI
    user_text = transcript.transcription["text"]

    # The response from GPT
    assistant_text = howie.response(from_user=user_text)

    if not to_console:
        print(f"From user to assistant: {user_text}")
        print(f"From assistant to user: {assistant_text}")


if __name__ == '__main__':
    main()
