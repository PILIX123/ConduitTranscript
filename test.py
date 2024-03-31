import torch
import whisper
from pyPodcastParser.Podcast import Podcast
from requests import get
import more_itertools
import threading
import time
import os

podcast = Podcast(get("https://www.relay.fm/conduit/feed").content)
l = list()
for filename in os.scandir("C:\\Users\\Server\\Desktop\\downloads"):
    if filename.is_file():
        l.append((filename.name,filename.path))
chunk = more_itertools.divide(torch.cuda.device_count(), l)

def startsWhisperSingle(device: int, episodeData: list):
    model = whisper.load_model("medium", f"cuda:{device}")
    for episode in episodeData:
        result = model.transcribe(episode[1])
        with open(f"{episode[0]}.txt", "w") as f:
            f.write(result["text"])

listThread = [threading.Thread(target=startsWhisperSingle,args=[x,chunk[x]]) for x in range(torch.cuda.device_count())]

for thread in listThread:
    thread.start()
    time.sleep(60)
time.sleep(300)