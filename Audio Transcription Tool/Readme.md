# Audio Transcription Tool

This Python script uses OpenAI's Whisper model to transcribe audio files.

## Prerequisites

- Python 3.6 or higher
- OpenAI API key

## Setup

1. Install the required package:

pip install openai

2. Set up your OpenAI API key:
- Sign up or log in at https://platform.openai.com/signup
- Generate a new API key from the "View API Keys" menu
- Add OPENAI_API_KEY as a secret in your environment or use a secrets management tool

## Usage

1. Place your audio file (e.g., "war_of_the_worlds.mp3") in the same directory as the script.
2. Run the script:

3. The transcript will be displayed in the console and saved to "transcript.txt".

## Notes

- This script uses the "whisper-1" model for transcription.
- Supported audio formats include mp3, mp4, mpeg, mpga, m4a, wav, and webm.
