import subprocess
import sys
import os
# import whisper

if __name__ == '__main__':
    # model = whisper.load_model("base")
    # result = model.transcribe("audio.wav")
    # print(result["text"])
    python_exec_path = sys.executable
    pro_plot = subprocess.run([python_exec_path, 'audio_realtimeplot.py'])

#    t1 = time.time()
#     model1 = whisper.load_model("tiny")
#     model2 = whisper.load_model("base")
#     model3 = whisper.load_model("small")
#     result1 = model1.transcribe("audio.wav", fp16=False)
#     result2 = model2.transcribe("audio.wav", fp16=False)
#     result3 = model3.transcribe("audio.wav", fp16=False)
#    t1_end = time.time()


#    print(t1_end-t1)

    # print(result1["text"])
    # print(result2["text"])
    # print(result3["text"])
    # os.remove('audio.wav')
    # print("audio.wav has been deleted")

