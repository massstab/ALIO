import subprocess
# import whisper

if __name__ == '__main__':
    # model = whisper.load_model("base")
    # result = model.transcribe("audio.wav")
    # print(result["text"])
    pro_plot = subprocess.run(['venv/bin/python3', 'audio_realtimeplot.py'])


