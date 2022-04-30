import numpy as np

from pedalboard import Pedalboard, load_plugin
from pedalboard.io import AudioFile
import time

soundfile = input("Input sound file: ")
step_size = 100
seconds_per_revolution = 6

print("Loading...")
dearvrmicro = load_plugin("vst\\dearVR MICRO.vst3")

board = Pedalboard([dearvrmicro,])

with AudioFile(soundfile, "r") as f:
    audio = f.read(f.frames)
    samplerate = f.samplerate

output_audio = np.zeros_like(audio)

print("Starting...")
start = time.time()

rotation = -180

for i in range(0, audio.shape[1], step_size):
    dearvrmicro.azimuth = np.clip(int(rotation), -180, 180)
    rotation = rotation + (360/seconds_per_revolution)/500 if rotation <= 180 else -180

    print(f"\r{round((i/audio.shape[1])*100)}% {round((audio.shape[1]-i)/((i+1)/(time.time()-start+0.01)))} seconds left...", end="", flush=True)

    chunk = board.process(audio[0:,i:i+step_size], samplerate, reset=False)
    output_audio[0:,i:i+step_size] = chunk

print(f"\rDone processing in {round(time.time()-start)}s", flush=True)
print("Writing to file...")

with AudioFile("(8D Audio) "+soundfile, "w", samplerate, output_audio.shape[0]) as f:
    f.write(output_audio)

print("Done")


