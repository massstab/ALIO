import subprocess
import sys
# import whisper

if __name__ == '__main__':
    # model = whisper.load_model("base")
    # result = model.transcribe("audio.wav")
    # print(result["text"])
    python_exec_path = sys.executable
    pro_plot = subprocess.run([python_exec_path, 'audio_realtimeplot.py'])



