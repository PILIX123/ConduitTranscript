import urllib.request
from pyPodcastParser.Podcast import Podcast
from requests import get

podcast = Podcast(get("https://www.relay.fm/conduit/feed").content)

episodeUrls = list()
for episode in podcast.items:
    t = episode.title.replace(":", "")
    t = t.replace("?","")
    tt = get(episode.enclosure_url)
    open(f"C:\\Users\\Server\\Desktop\\downloads\\{t}.mp3","wb").write(tt.content)

