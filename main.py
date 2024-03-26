from pyPodcastParser.Podcast import Podcast
from requests import get
import whisper

podcast = Podcast(get("https://www.relay.fm/conduit/feed").content)

episodeUrls = []
for episode in podcast.items:
    episodeUrls.append((episode.title, episode.enclosure_url))

t = episodeUrls[0][0]
with open(f"{t}.txt", "w") as file:
    file.write("text")
model = whisper.load_model("large", device="cuda:0")
result = model.transcribe(episodeUrls[0][1])
