import os
import array
import torch
from russtress import Accent

accent = Accent()



device = torch.device('cpu')
torch.set_num_threads(4)
LOCAL_FILE = 'model.pt'

if not os.path.isfile(LOCAL_FILE):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                   LOCAL_FILE)  

model = torch.package.PackageImporter(LOCAL_FILE).load_pickle("tts_models", "model")
model.to(device)

SAMPLE_RATE = 48000
SPEAKER='baya'


def tts(text):
    print(text)
    text = accent.put_stress(text)
    while text.find("'") != -1:
        index = text.find("'")
        s = array.array('u', text)
        s.insert(index-1, "+")
        s.pop(index+1)
        text = s.tounicode()

    audio = model.apply_tts(text=text,
                             speaker=SPEAKER,
                             sample_rate=SAMPLE_RATE)
    return audio
  