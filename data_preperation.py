import h5_getter
import numpy as np
import os
import pypianoroll
import pandas as pd
import pretty_midi
import matplotlib.pyplot as plt
import librosa
import music21

root_dir = '.'
data_dir = root_dir + '/dataset/lpd_5_cleansed'
music_dataset_lpd_dir = root_dir + '/dataset/lmd_matched_h5'

cleansed_ids = pd.read_csv(os.path.join('dataset', 'cleansed_ids.txt'), delimiter = '    ', header = None)
lpd_to_msd_ids = {a:b for a, b in zip(cleansed_ids[0], cleansed_ids[1])}
msd_to_lpd_ids = {a:b for a, b in zip(cleansed_ids[1], cleansed_ids[0])}

RESULTS_PATH = os.path.join(root_dir, 'dataset')

# Utility functions for retrieving paths
def msd_id_to_dirs(msd_id):
    """Given an MSD ID, generate the path prefix.
    E.g. TRABCD12345678 -> A/B/C/TRABCD12345678"""
    return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)


def msd_id_to_h5(msd_id):
    """Given an MSD ID, return the path to the corresponding h5"""
    return os.path.join(RESULTS_PATH, 'lmd_matched_h5',
                        msd_id_to_dirs(msd_id) + '.h5')

# Load the midi npz file from the LMD cleansed folder
def get_midi_npz_path(msd_id, midi_md5):
    return os.path.join(data_dir,
                        msd_id_to_dirs(msd_id), midi_md5 + '.npz')
    
# Load the midi file from the Music Dataset folder
def get_midi_path(msd_id, midi_md5):
    return os.path.join(music_dataset_lpd_dir,
                        msd_id_to_dirs(msd_id), midi_md5 + '.mid')

# Reading the genre annotations
genre_file_dir = os.path.join('dataset', 'msd_tagtraum_cd1.cls')
ids = []
genres = []
with open(genre_file_dir) as f:
    line = f.readline()
    while line:
        if line[0] != '#':
          split = line.strip().split("\t")
          if len(split) == 2:
            ids.append(split[0])
            genres.append(split[1])
          elif len(split) == 3:
            ids.append(split[0])
            ids.append(split[0])
            genres.append(split[1])
            genres.append(split[2])
        line = f.readline()
genre_df = pd.DataFrame(data={"TrackID": ids, "Genre": genres})

# get ids of pop songs
pop_ids = genre_df[genre_df['Genre'] == 'Pop_Rock']['TrackID'].tolist()

pop_lpd_ids = [msd_to_lpd_ids[msd_id] for msd_id in pop_ids if msd_id in msd_to_lpd_ids]

notes = []

i = 0
for lpd_file_name in pop_lpd_ids:
    msd_file_name = lpd_to_msd_ids[lpd_file_name]

    # Get the NPZ path
    npz_path = get_midi_npz_path(msd_file_name, lpd_file_name)

    multitrack = pypianoroll.load(npz_path)
    pm = pypianoroll.to_pretty_midi(multitrack)
    new_midi_path = npz_path[:-4] + '.mid'
    pypianoroll.write(new_midi_path, multitrack)
    # Get the MIDI path (should already be generated)
    new_midi_path = npz_path[:-4] + '.mid'
    midi = music21.converter.parse(new_midi_path)

    s2 = music21.instrument.partitionByInstrument(midi)
    piano_part = None
    # Filter for  only the piano part
    instr = music21.instrument.Piano
    for part in s2:
        if isinstance(part.getInstrument(), instr):
            piano_part = part

    notes_song = []
    if piano_part: # Some songs somehow have no piano parts
        for element in piano_part:
            if isinstance(element, music21.note.Note):
            # Return the pitch of the single note
                notes_song.append(str(element.pitch))
            elif isinstance(element, music21.chord.Chord):
            # Returns the normal order of a Chord represented in a list of integers
                notes_song.append('.'.join(str(n) for n in element.normalOrder))

    notes.append(notes_song)
    i+=1
    print(i)