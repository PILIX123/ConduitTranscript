import whisper
from pyPodcastParser.Podcast import Podcast
from requests import get


conduit = Podcast(get("https://www.relay.fm/conduit/feed").content)
latestEpisode = conduit.items[0]
newTitle = latestEpisode.title.replace(":", "")
newTitle = newTitle.replace("?", "")
episodeData = (newTitle, latestEpisode.enclosure_url)
model = whisper.load_model("large", "cuda:0")
result = model.transcribe(episodeData[1])
with open(f"{episodeData[0]}.mp3.txt", "w") as f:
    f.write(result["text"])
