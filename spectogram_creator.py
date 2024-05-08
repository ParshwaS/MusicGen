from riffusion_helper.spectrogram_image_converter import SpectrogramImageConverter
from riffusion_helper.spectrogram_params import SpectrogramParams
import os
import pydub
from glob import glob

params = SpectrogramParams()

converter = SpectrogramImageConverter(params=params)

def save_spectrogram_image_from_audio(filename: str):

    audio = pydub.AudioSegment.from_file(f'{filename}')

    print(len(audio))

    name = filename.split('/')[-1].split('.')[0]

    for i in range(0, len(audio), 5000):
        clip = audio[i:i+5000]
        image = converter.spectrogram_image_from_audio(clip)
        image.save(f'./dataset/spectrograms/{name}_{i}.png')
        print(f'./dataset/spectrograms/{name}_{i}.png')
    
    return True

# Load all files with .mid from dataset folder

# datadir = './dataset/lpd_5_cleansed'

# files = glob(f'{datadir}/A/A/A/*/*.mid')

# print(files)

# for file in files:
save_spectrogram_image_from_audio("./output.mp3")
    # break

print('Done')