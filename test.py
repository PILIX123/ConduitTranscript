import torch
import whisper
from pyPodcastParser.Podcast import Podcast
from requests import get
import more_itertools
import threading
import time
import io

podcast = Podcast(get("https://www.relay.fm/conduit/feed").content)

episodeUrls = list()
for episode in podcast.items:
    episodeUrls.append((episode.title, episode.enclosure_url))

chunk = more_itertools.divide(torch.cuda.device_count(), episodeUrls)

def startsWhisperSingle(device: int, episodeData: list[tuple[str, str]]):
    model = whisper.load_model("medium", f"cuda:{device}")
    for episode in episodeData:
        t = episode[0].replace(":", "")
        time.sleep(10*device)
        result = model.transcribe(episode[1])
        with open(f"{t}.txt", "w") as f:
            f.write(result["text"])

listThread = [threading.Thread(target=startsWhisperSingle,args=[x,chunk[x]]) for x in range(torch.cuda.device_count())]

for thread in listThread:
    thread.start()
time.sleep(500)