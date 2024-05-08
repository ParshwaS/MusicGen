# Using matplotlib to create a waveform from an audio file mp3

import matplotlib.pyplot as plt
import numpy as np
import pydub

audio = pydub.AudioSegment.from_file("soothingSlowMusic.mp3")
samples = audio.get_array_of_samples()
samples = np.array(samples)
timeseries = np.linspace(0, len(samples) / audio.frame_rate, num=len(samples))
plt.plot(timeseries, samples, color='tab:blue')
plt.xlabel('Time')
plt.ylabel('Amplitude')
# Make sure plot is not cut off
plt.tight_layout()
plt.savefig("soothingSlowMusicWaveform.pdf", format='pdf')