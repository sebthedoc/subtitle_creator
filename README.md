# Subtitle Creator

This project provides various tools for creating subtitles from video or audio files using different transcription methods.

## Features

- Transcribe audio/video files to SRT subtitle format
- Support for multiple languages (including auto-detection)
- Options for local processing or cloud-based transcription
- Utilizes OpenAI's Whisper model and Groq's API

## Scripts


### 1. sub_groq.py

Uses the Groq API for cloud-based transcription.

Usage:
```
python sub_groq.py [file]
python sub_groq.py [file] -no  # Skip audio extraction
```

Requirements:
- Groq API key (set in .env file)

### 2. sub_local_whisper_large.py

Uses the large Whisper model for local transcription.

Usage:
```
python sub_local_whisper_large.py [file]
```

### 3. sub_local_whisper.py

Uses the base Whisper model for faster local transcription.

Usage:
```
python sub_local_whisper.py [file]
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/sebthedoc/subtitle_creator.git
   ```

2. Install the required dependencies:
   ```
   pip install whisper openai-whisper groq python-dotenv
   ```

3. For sub_groq.py, create a .env file in the project root and add your Groq API key:
   ```
   API_KEY=your_groq_api_key_here
   ```

## Dependencies

- whisper
- groq
- python-dotenv
- ffmpeg (for audio extraction)

## Notes

- The scripts will generate .srt files in the same directory as the input file.
- Some scripts also generate .json files with detailed transcription information.
- Processing time may vary depending on the chosen method and file size.

## License

This project is licensed under the BSD 2-Clause License. See the [LICENSE](LICENSE) file for details.

## Authors

See the [AUTHORS](AUTHORS) file for a list of contributors to this project.

## Contributing


## Issues

If you encounter any problems or have suggestions, please open an issue on the GitHub repository.

## Contact

For questions or feedback, please open an issue on this GitHub repository.