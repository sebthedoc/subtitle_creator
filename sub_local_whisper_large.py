import json
import sys
import os
import whisper
import json # used to visualize output
from typing import Iterator, TextIO
import time

import warnings
# whisper
warnings.filterwarnings("ignore", category=FutureWarning)


def vid_to_audio(file):
    '''extract audio from video using ffmpeg'''
    os.sys("ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn audio.mp3".format(file))
    return



def whisper_transcribe_en(file="{}/audio.mp3".format(dir)):
    '''transcribe audio to text using whisper'''
    #model = whisper.load_model("base")
    #model = whisper.load_model("small")
    #model = whisper.load_model("medium")
    model = whisper.load_model("large")
    #result = model.transcribe(file, fp16 = False, language="English")
    result = model.transcribe(file, fp16 = False, language="Finnish")
    json_object = json.dumps(result, indent=4)
    return result, json_object



def format_timestamp(seconds: float, always_include_hours: bool = False):
    '''format timestamp to SRT format'''
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def write_srt(transcript: Iterator[dict], file: TextIO):
    '''write transcript to SRT file'''
    for i, segment in enumerate(transcript, start=1):
        print(
            f"{i}\n"
            f"{format_timestamp(segment['start'], always_include_hours=True)} --> "
            f"{format_timestamp(segment['end'], always_include_hours=True)}\n"
            f"{segment['text'].strip().replace('-->', '->')}\n",
            file=file,
            flush=True,
        )


if __name__ == "__main__":
    '''main function'''
    print("Getting working directory...")
    #dir = get_working_dir()

    file = sys.argv[1]
    name, _ = os.path.splitext(file)
    name = f"{name}.srt"
    print("Transcribing {} to {}...".format(file, name))

    start_time = time.time()


    result, json_object = whisper_transcribe_en(file)


    # Assuming result is a dictionary
    result_dict = result.to_dict() if hasattr(result, "to_dict") else result

    # Store the result as a JSON file
    with open(f"{name}.json", "w") as json_file:
        json.dump(result_dict, json_file, indent=4)



    print("Turning transcription into SRT subtitle file... ")
    #whisper_result_to_srt(result) 
    '''converts whisper result to SRT format'''

    with open(name, "w", encoding="utf-8") as srt:
        write_srt(result["segments"], file=srt)
        
    end_time = time.time()
    runtime = end_time - start_time
     
    print("Done, saved to {}".format(name))
    print("Runtime: {} seconds, or {} minutes".format(runtime, runtime/60))
