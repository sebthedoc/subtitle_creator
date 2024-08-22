import os, sys, subprocess
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")

client = Groq(api_key=API_KEY)

filename = sys.argv[1]
name, _ = os.path.splitext(filename)
print("Transcribing {} to {}.srt / .json...".format(filename, name))


if len(sys.argv) > 1 and (len(sys.argv) < 3 or sys.argv[2] != "-no"):    
    # Extract audio from video file
    audio_filename = f"{name}_output.mp3"
    ffmpeg_command = [
        "ffmpeg",
        "-y",  # Overwrite output files without asking
        "-i",
        filename,
        "-vn",
        "-c:a",
        "libmp3lame",
        #"-b:a",
        #"12k", # GSM audio kbps
        #"-ar",
        #"8000", # Hz, typical phone
        "-ac",
        "1",
        audio_filename,
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Audio extracted to {audio_filename}")
        filename = audio_filename
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
        sys.exit(1)


# Function to format timestamp to SRT format
def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"



# Process the file and store the transcription
with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="whisper-large-v3",
        prompt="Specify context or spelling",  # Optional
        response_format="verbose_json",  # Optional
        # language="en",  # Optional
        temperature=0.0,  # Optional
    )

    # Assuming the transcription object has a method to get a dictionary
    transcription_dict = (
        transcription.to_dict() if hasattr(transcription, "to_dict") else transcription
    )

    # Store the transcription as a JSON file
    with open(f"{name}.json", "w") as json_file:
        json.dump(transcription_dict, json_file, indent=4)

    print("Transcription text:", transcription_dict["text"])

    # Print timestamps and attempt to create an SRT file
    with open(f"{name}.srt", "w") as srt_file:
        for i, segment in enumerate(transcription_dict["segments"], start=1):
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]

            # Print timestamps
            print(f"Segment {i}: Start={start_time}, End={end_time}, Text={text}")

            # Write SRT file content
            srt_file.write(f"{i}\n")
            srt_file.write(
                f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n"
            )
            srt_file.write(f"{text.strip()}\n\n")
