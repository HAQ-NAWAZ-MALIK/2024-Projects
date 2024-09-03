# h.AI  Voice Assistant

  ![HIA.gif](https://github.com/HAQ-NAWAZ-MALIK/2024-Projects/blob/main/AI%20LiveKit%20Voice%20Assistant/HIA.gif)
  
This project implements a voice assistant using the LiveKit platform. The assistant can interact with users via voice and text chat in Real Time a LiveKit room.
It uses Deepgram for speech-to-text, OpenAI for the language model and text-to-speech, and Silero for voice activity detection.
## Features

- Voice-based interaction
- Text chat support
- Speech-to-text (STT) using Deepgram
- Text-to-speech (TTS) using OpenAI
- Language model (LLM) for generating responses using OpenAI
- Voice Activity Detection (VAD) using Silero

## Prerequisites

- Python 3.7+
- LiveKit SDK
- OpenAI API key
- Deepgram API key

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install livekit deepgram-sdk openai python-dotenv
   ```
3. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   ```

## Usage

Run the script using:

```
python Voice.py
```

## Code Structure

- `prewarm_process`: Preloads the Silero VAD model for faster session start.
- `handle_participant`: Manages the interaction with a participant, including voice and chat.
- `entrypoint`: Sets up the room connection and participant handling.
- `VoiceAssistant`: Core class that integrates STT, TTS, LLM, and VAD for voice interaction.

## Configuration

The voice assistant is configured with the following components:
- VAD: Silero
- STT: Deepgram
- LLM: OpenAI
- TTS: OpenAI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
"MIT"
