from config import *
from pydub import AudioSegment
from pydub.silence import split_on_silence
import matplotlib.pyplot as plt

def test(audio_path):
    print("Reading in the wave file...")
    seg = AudioSegment.from_file(audio_path)

    print("Information:")
    print("Channels:", seg.channels)
    print("Bits per sample:", seg.sample_width * 8)
    print("Sampling frequency:", seg.frame_rate)
    print("Length:", seg.duration_seconds, "seconds")


audio_dir = os.path.join(Path.root, 'audio_data')
audio_list = os.listdir(audio_dir)

audio_info = dict()
def read_data_info():
    with open(os.path.join(Path.root, "audio_data_info.txt"), "r") as f:
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


def match_target_amplitude(aChunk, target_dBFS):
    # Normalize given audio chunk
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


def visualize(spect, frequencies, title=""):
    # Visualize the result of calling seg.filter_bank() for any number of filters
    i = 0
    for freq, (index, row) in zip(frequencies[::-1], enumerate(spect[::-1,])):
        plt.subplot(spect.shape[0], 1, index + 1)
        if i == 0:
            plt.title(title)
            i += 1
        plt.ylabel("{0:.0f}".format(freq))
        plt.plot(row)
    plt.show()


def process_audio():
    for audiofile in audio_list:
        if not audiofile.endswith("wav"):
            continue
        basename, ext = os.path.splitext(audiofile)

        if os.path.exists(os.path.join(Path.root, "output", basename)):
            continue

        print("Start process audiofile: {0}".format(os.path.join(Path.root, audio_dir, audiofile)))
        idx = 0
        audio = AudioSegment.from_file(os.path.join(Path.root, audio_dir, audiofile), ext)
        chunks = split_on_silence(audio, min_silence_len=100, silence_thresh=-30)
        print("Count of chunk is {0}".format(len(chunks)))
        for i, chunk in enumerate(chunks):
            silence_chunk = AudioSegment.silent(duration=500)
            audio_chunk = silence_chunk + chunk + silence_chunk
            normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

            if idx < len(audio_info[audiofile]):
                output_audio_name = audio_info[audiofile][idx]
            else:
                output_audio_name = "{0}_{1}".format(basename, idx)

            print("Exporting {0}{1}.".format(output_audio_name, Extensions.ogg))
            idx += 1
            dirname = os.path.join(Path.root, os.path.join("output", basename))
            os.makedirs(dirname, exist_ok=True)
            with open("{0}{1}".format(os.path.join(dirname, output_audio_name), Extensions.ogg), "wb") as f:
                normalized_chunk.export(f, # bitrate="192k",
                format="ogg")


if __name__ == "__main__":
    read_data_info()
    process_audio()

