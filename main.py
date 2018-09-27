# import pyaudio
# import wave
#
# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 2
# RATE = 44100
# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "output.wav"
#
# p = pyaudio.PyAudio()
#
# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 frames_per_buffer=CHUNK)
#
# print("* recording")
#
# frames = []
#
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
#
# print("* done recording")
#
# stream.stop_stream()
# stream.close()
# p.terminate()
#
# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()


from pydub import AudioSegment

# # wav_audio = AudioSegment.from_file("aa.ogg")
# raw_audio = AudioSegment.from_file("aa.ogg")
# # wav_audio.export("audio1.mp3", format="mp3")
# raw_audio.export("audio2.mp3", format="mp3")

import speech_recognition as sr

# Record Audio
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
print(type(audio))
print(type(source))
# Speech recognition using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("You said: " + r.recognize_google(audio,language="fa-IR"))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))