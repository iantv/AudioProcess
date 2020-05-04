import subprocess
import os
from pydub import AudioSegment
import ffmpeg

root = os.path.dirname(os.path.abspath(__file__))
odir = "ogg"
audio_dir = os.path.join(root, 'audio_data')
os.makedirs(os.path.join(root, odir), exist_ok=True)
audio_list = os.listdir(audio_dir)


audio_info = dict()
def read_data_info():
    with open(os.path.join(root, "audio_data_info.txt"), "r") as f:
        lines = f.read().splitlines()
        for phrase in lines: # lines: ['#AUDIO Recording 1.m4a', 'Hello', 'Good_afternoon', 'Can_I_have one apple please?' ... ]
            words = phrase.split(' ')
            if words[0] == "#AUDIO":
                keyword = " ".join(words[1:3])
                print(keyword)
                print(audio_info)
                continue
            elif words[0] == '' or words[0][0] == "#":
                print("Skipped word {0}".format(words))
            else:
                if not keyword in audio_info:
                    audio_info[keyword] = list()
                audio_info[keyword].extend(words)
                print("Added value={0} with key={1}".format(words, keyword))
    print(audio_info)


def process_audio():
    for audiofile in audio_list:
        if not audiofile.endswith("m4a"):
            continue
        basename, ext = os.path.splitext(audiofile)
        print(os.path.join(root, audio_dir, audiofile))
        audio = AudioSegment.from_file(os.path.join(root, audio_dir, audiofile), ext)
        os.makedirs(basename, exist_ok=True)
        audio.export(os.path.join("output", basename), format="ogg")
        #break


if __name__ == "__main__":
    read_data_info()
    process_audio()

