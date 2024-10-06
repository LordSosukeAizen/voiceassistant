import whisper
import os
import pyaudio
import time
import warnings
import wave
import sys
from gpt4all import GPT4All
import pyautogui
import webbrowser as wb
import pyttsx3

# Suppress the specific FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)



# Load the Whisper model
base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
model = whisper.load_model(base_model_path)




# Initialize the TTS engine
engine = pyttsx3.init()

# Set properties before adding anything to speak
engine.setProperty('rate', 150)  # Speed percent (can go over 100)
engine.setProperty('volume', 1)  # Volume 0-1

# Set to a female voice (you may need to adjust the voice ID)
engine.setProperty('voice', 'com.apple.voice.compact.en-AU.Karen')
# for voice in voices:
#     if 'female' in voice.name.lower():  # Modify this condition based on available voices
#         engine.setProperty('voice', voice.id)

def respond(text):
    ALLOWED_CHARS = set('abcdegfhijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,/?!$@+-')
    clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
    
    
    engine.say(clean_text)
    engine.runAndWait()

# VOICEBOT NAME
NAME = ''

gpt = GPT4All("/Users/praneethsai/.cache/gpt4all/Meta-Llama-3-8B-Instruct.Q4_0.gguf")


# Audio settings
RATE = 16000
FORMAT = pyaudio.paInt16
FRAMES_PER_BUFFER = 1024
CHANNELS = 1
SEC = 9
def listen_for_command():
    p = pyaudio.PyAudio()
    stream = p.open(
        channels=CHANNELS,
        rate=RATE,
        format=FORMAT,
        frames_per_buffer=FRAMES_PER_BUFFER,
        input=True
    )
    
    print('Listening for command...')
    
    # Record audio for a fixed duration
    audio_data = []
    for _ in range(0, int(RATE / FRAMES_PER_BUFFER * SEC)):  # 5 seconds
        data = stream.read(FRAMES_PER_BUFFER)
        audio_data.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a file
    audiofile = "recording.wav"
    audio = wave.open(audiofile, "wb")
    audio.setnchannels(1)
    audio.setframerate(16000)
    audio.setsampwidth(p.get_sample_size(FORMAT))
    audio.writeframes(b''.join(audio_data))
    audio.close()

    # Transcribe the audio
    command = model.transcribe(audiofile, language='en')
    
    # Print the transcribed text
    if command and command['text']:
        print('Me:', command['text'])
        return command['text']
    else:
        print('Not transcribable')
    os.remove(audiofile)


def respond_for_command(command):
    
    
    command = command.strip(' ').lower()
    if command == "who are you?" :
        respond('Iam Karen your virtual assistant how can i help you?')

    elif command == 'open google':
        wb.open('https://www.google.co.in/?client=safari&channel=mac_bm')
        respond('Opend Google')
    elif command == 'open youtube':
        wb.open('https://www.youtube.com/')
        respond('Opened youtube')
    elif command == 'open chatgpt':
        wb.open('https://chatgpt.com/')
        respond('Opened chatgpt')
    else:
        respond('Thinking')
        with gpt.chat_session():
            output = gpt.generate(command)
        print('BOT: ', output)
        respond(output)
    
        


if __name__ == '__main__':
    
    transcripted = listen_for_command()
    respond_for_command(transcripted)
    
