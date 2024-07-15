import os
import sys
import pyaudio
import wave
from threading import Thread
import speech_recognition as sr

import assemblyai as aai

import pyautogui


aai.settings.api_key = sys.argv[1]
transcriber = aai.Transcriber()

CHUNK = 1024  
FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 44100  
RECORD_SECONDS = 5  

recognizer = sr.Recognizer()



def transcribe(audio_filename):
    try:
        transcript = transcriber.transcribe(audio_filename)
        pyautogui.write(transcript.text.lower()[:-1]+' ')
        os.remove(audio_filename)
        if "stop recording" in transcript.text.lower():
            for file in os.listdir("/tmp/recordings"):
                os.remove(f"/tmp/recordings/{file}")
            print("Stopping recording...")
            os._exit(0)
    except Exception as e:
        print(f"Could not request results from speech recognition service: {e}")
        os.remove(audio_filename)


if not os.path.exists("/tmp/recordings"):
    os.makedirs("/tmp/recordings")


audio_index = 0
while True:
    audio_index += 1
    audio_filename = f"/tmp/recordings/recording_{audio_index}.wav"
    frames = []

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print(f"Recording {audio_filename}...")
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    
    wf = wave.open(audio_filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    print(f"Finished recording {audio_filename}")

    
    
    Thread(target=transcribe, args=(audio_filename,)).start()

    
    