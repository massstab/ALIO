import subprocess
import sys
import os
import whisper
import openai
import datetime

if __name__ == '__main__':
    # model = whisper.load_model("base")
    # result = model.transcribe("audio.wav")
    # print(result["text"])
    python_exec_path = sys.executable
    pro_plot = subprocess.run([python_exec_path, 'audio_realtimeplot.py'])

    # model1 = whisper.load_model("tiny")
    model2 = whisper.load_model("base")
#     model3 = whisper.load_model("small")
#     result1 = model1.transcribe("audio.wav", fp16=False)
    result2 = model2.transcribe("audio.wav", fp16=False)
#     result3 = model3.transcribe("audio.wav", fp16=False)

    openai.api_key = "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"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=result2["text"],
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    question = result2["text"]
    answer = response["choices"][0]["text"][2:]
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    with open("log.txt", "a") as log_file:
        log_file.write(dt_string + " - " + "Question: " + question + "\n" + dt_string + " - " + "Answer: " + answer + "\n")

    print(f"Question: {question}")
    print(f"Answer: {answer}")

    os.remove('audio.wav')
    print("audio.wav has been deleted")

