from sys import argv
from enum import Enum, auto
from moviepy.editor import VideoFileClip, concatenate_videoclips

class Output(Enum):
    VIDEO = auto()
    AUDIO = auto()

def write(clip, out_f: str, out_t):
    match out_t:
        case Output.VIDEO:
            clip.write_videofile(out_f, codec="libx264")
        case Output.AUDIO:
            clip.write_audiofile(out_f)

def to_clip(filename: str):
    return VideoFileClip(filename)


def trim_clip(filename: str, start=0, end=None):
    return to_clip(filename).subclip(start, end)


def extract_audio(c):
    return c.audio


def concatenate_clips(filenames):
    clips = [to_clip(f) for f in filenames] 
    return concatenate_videoclips(clips)


def help():
    print('Smol tool to trim, merge and extract audios from videos.')
    print('usage: Chickenfoot [-t in out start end] [-a in out {start end}] [-m ins... out]')
    print('options:\n\t-h\t\t\tshow this help message and exit')
    print('\t-t in out start end\ttrim video or audio. Eg start and end: "00:00:03.00" "00:00:06.00"')
    print('\t-a in out {start end}\textract audio. optional: trim with given start and end')
    print('\t-m ins... out\t\tmerge two or more inputs.')


def main():
    match argv[1:]:
        case []:
            print('missing argument, -h for help.')

        case ['-h']:
            help()

        case ['-t', filename, out, start, end]:
            print(f'trimming {filename} [{start}...{end}] -> {out}\n...\n')
            write(trim_clip(filename, start, end), out, Output.VIDEO)

        case ['-a', filename, out, *optional]:
            if optional:
                if len(optional) == 2: # trim
                    start, end = optional
                    print(f'extracting {filename} [{start}...{end}] -> {out}\n...\n')
                    write(extract_audio(trim_clip(filename, start, end)),
                          out,
                          Output.AUDIO
                    )
                else:
                    print(f"error parsing argument: {argv[1:]}. Not Enough or Too many arguments.")
            else:
                print(f'extracting {filename} -> {out}\n...\n')
                write(extract_audio(to_clip(filename)), out, Output.AUDIO)

        case ['-m', *inputs, out]:
            if len(inputs) < 2:
                print(f"not enough files to merge: {len(inputs)}")
            else:
                print(f"merging {inputs} -> {out}\n...\n")
                write(concatenate_clips(inputs), out, Output.VIDEO)

        case _:
            print(f"Sorry, I couldn't understand: {argv[1:]}. Perhaps inputs are missing.")
            

if __name__ == "__main__":
    main()
