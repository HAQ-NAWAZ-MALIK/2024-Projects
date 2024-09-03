import os
from livekit_plugins_openai import STTClient, TTSClient, DALL_E_Client

# Ensure the API key is set
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key is not set. Please set the OPENAI_API_KEY environment variable.")

# Initialize clients for each service
stt_client = STTClient(api_key=api_key)
tts_client = TTSClient(api_key=api_key)
dalle_client = DALL_E_Client(api_key=api_key)

# Example usage for Speech-to-Text (STT)
audio_file_path = 'path_to_audio_file.wav'
text = stt_client.convert_speech_to_text(audio_file_path)
print(f"Transcribed text: {text}")

# Example usage for Text-to-Speech (TTS)
text_to_speak = "Hello, how can I assist you today?"
audio_output_path = 'output_audio.wav'
tts_client.convert_text_to_speech(text_to_speak, audio_output_path)
print(f"Audio saved to: {audio_output_path}")

# Example usage for DALL·E 3
prompt = "A futuristic city skyline at sunset"
image_path = 'output_image.png'
dalle_client.generate_image(prompt, image_path)
print(f"Generated image saved to: {image_path}")
