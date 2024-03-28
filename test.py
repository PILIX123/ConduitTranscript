import torch
import whisper
from pyPodcastParser.Podcast import Podcast
from requests import get
import more_itertools
import threading
import time

podcast = Podcast(get("https://www.relay.fm/conduit/feed").content)

episodeUrls = list()
for episode in podcast.items:
    episodeUrls.append((episode.title, episode.enclosure_url))

chunk = more_itertools.divide(torch.cuda.device_count(), episodeUrls)
listModel = list()
for device in range(torch.cuda.device_count()):
    listModel.append(whisper.load_model("medium", f"cuda:{device}"))


def startsWhisperSingle(model: whisper.Whisper, episodeData: tuple[str, str]):
    result = model.transcribe(episodeData[1])
    t = episodeData[0].replace(":", "")
    with open(f"{t}.txt", "w") as f:
        f.write(result["text"])


listListThreadsModel = list()
for x in range(torch.cuda.device_count()):
    listListThreadsModel.append([threading.Thread(target=startsWhisperSingle, args=[
        listModel[x], episodeContent]) for episodeContent in chunk[x]])

working = True
listT = list()
for x in listListThreadsModel:
    listT.append(x[0])

for t in listT:
    t.start()

while working:
    for i, t in enumerate(listT):
        if not t.is_alive():
            if len(listListThreadsModel[i]) == 0:
                continue
            listListThreadsModel[i].pop(0)
            t = listListThreadsModel[i][0]
            t.start()

    x = 0
    for l in listListThreadsModel:
        if len(l) == 0:
            x += 1
    if x == len(listListThreadsModel):
        working = False
    time.sleep(300)
