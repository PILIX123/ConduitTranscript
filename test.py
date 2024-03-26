import torch
import whisper
from pyPodcastParser.Podcast import Podcast
from requests import get
import more_itertools
import threading

podcast = Podcast(get("https://www.relay.fm/conduit/feed").content)

episodeUrls = list()
for episode in podcast.items:
    episodeUrls.append((episode.title, episode.enclosure_url))

chunk = more_itertools.divide(8, episodeUrls)
listModel = list()
for device in range(torch.cuda.device_count()):
    listModel.append(whisper.load_model("medium", f"cuda:{device}"))


def startsWhisperSingle(model: whisper.Whisper, episodeData: tuple[str, str]):
    result = model.transcribe(episodeData[1])
    t = episodeData[0].replace(":", "")
    with open(f"{t}.txt", "w") as f:
        f.write(result["text"])


listThreadsModel1 = [threading.Thread(target=startsWhisperSingle, args=[
    listModel[0], episodeContent]) for episodeContent in chunk[0]]
listThreadsModel2 = [threading.Thread(target=startsWhisperSingle, args=[
    listModel[1], episodeContent]) for episodeContent in chunk[1]]
listThreadsModel3 = [threading.Thread(target=startsWhisperSingle, args=[
    listModel[2], episodeContent]) for episodeContent in chunk[2]]
listThreadsModel4 = [threading.Thread(target=startsWhisperSingle, args=[
    listModel[3], episodeContent]) for episodeContent in chunk[3]]
listThreadsModel5 = [threading.Thread(target=startsWhisperSingle, args=[
    listModel[4], episodeContent]) for episodeContent in chunk[4]]
listThreadsModel6 = [threading.Thread(target=startsWhisperSingle, args=[
    listModel[5], episodeContent]) for episodeContent in chunk[5]]
listThreadsModel7 = [threading.Thread(target=startsWhisperSingle, args=[
    listModel[6], episodeContent]) for episodeContent in chunk[6]]
listThreadsModel8 = [threading.Thread(target=startsWhisperSingle, args=[
    listModel[7], episodeContent]) for episodeContent in chunk[7]]

working = True
t1 = listThreadsModel1[0]
t2 = listThreadsModel2[0]
t3 = listThreadsModel3[0]
t4 = listThreadsModel4[0]
t5 = listThreadsModel5[0]
t6 = listThreadsModel6[0]
t7 = listThreadsModel7[0]
t8 = listThreadsModel8[0]

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()

while working:
    if not t1.is_alive():
        listThreadsModel1.pop(0)
        t1 = listThreadsModel1[0]
        t1.start()
    if not t2.is_alive():
        listThreadsModel2.pop(0)
        t2 = listThreadsModel2[0]
        t2.start()
    if not t3.is_alive():
        listThreadsModel3.pop(0)
        t3 = listThreadsModel3[0]
        t3.start()
    if not t4.is_alive():
        listThreadsModel4.pop(0)
        t4 = listThreadsModel4[0]
        t4.start()
    if not t5.is_alive():
        listThreadsModel5.pop(0)
        t5 = listThreadsModel5[0]
        t5.start()
    if not t6.is_alive():
        listThreadsModel6.pop(0)
        t6 = listThreadsModel6[0]
        t6.start()
    if not t7.is_alive():
        listThreadsModel7.pop(0)
        t7 = listThreadsModel7[0]
        t7.start()
    if not t8.is_alive():
        listThreadsModel8.pop(0)
        t8 = listThreadsModel8[0]
        t8.start()

    if len(listThreadsModel8) != 0 or len(listThreadsModel7) != 0 or len(listThreadsModel6) != 0 or len(listThreadsModel5) != 0 or len(listThreadsModel4) != 0 or len(listThreadsModel3) != 0 or len(listThreadsModel2) != 0 or len(listThreadsModel1) != 0:
        working = False
