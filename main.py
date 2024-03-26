from pyPodcastParser.Podcast import Podcast
from requests import get
import whisper


def startsWhisperSingle(model: whisper.Whisper, episodeData: tuple[str, str]):
    result = model.transcribe(episodeData[1])
    t = episodeData[0].replace(":", "")
    with open(f"{t}.txt", "w") as f:
        f.write(result["text"])


def startWhisperMulti(device1: str, device2: str, episodeData: tuple[str, str]):
    model = whisper.load_model("large", device="cpu")

    model.encoder.to(device1)
    model.decoder.to(device2)

    model.decoder.register_forward_pre_hook(lambda _, inputs: tuple(
        [inputs[0].to(device2), inputs[1].to(device2)] + list(inputs[2:])))
    model.decoder.register_forward_hook(
        lambda _, inputs, outputs: outputs.to(device1))

    result = model.transcribe(episodeData[1])
    t = episodeData[0].replace(":", "")
    with open(f"{t}.txt", "w") as f:
        f.write(result["text"])


def test():
    return "test"


podcast = Podcast(get("https://www.relay.fm/conduit/feed").content)

episodeUrls = list()
for episode in podcast.items:
    episodeUrls.append((episode.title, episode.enclosure_url))
