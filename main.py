from pyPodcastParser.Podcast import Podcast
from requests import get
import whisper
import torch

podcast = Podcast(get("https://www.relay.fm/conduit/feed").content)

episodeUrls = []
for episode in podcast.items:
    episodeUrls.append(episode.enclosure_url)

model = whisper.load_model("large", device="cuda:0")
result = model.transcribe(episodeUrls[0])
print(result["text"])
