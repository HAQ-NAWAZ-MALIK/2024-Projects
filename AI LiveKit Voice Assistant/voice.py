import asyncio
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, openai, silero

# Load environment variables from a .env file
load_dotenv()

async def entrypoint(ctx: JobContext):
    # Define the initial chat context for the assistant
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant. Your interactions with users will be voice-based. "
            "Keep your responses brief and clear, avoiding unpronounceable punctuation."
        ),
    )

    # Connect to the context with automatic audio subscription
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Set up the voice assistant with voice activity detection, speech-to-text, and text-to-speech functionalities
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
    )

    # Start the assistant in the connected room
    assistant.start(ctx.room)

    # Manage incoming chat messages (optional if the agent should respond to text-based chat)
    chat = rtc.ChatManager(ctx.room)

    async def answer_from_text(txt: str):
        chat_ctx = assistant.chat_ctx.copy()
        chat_ctx.append(role="user", text=txt)
        stream = assistant.llm.chat(chat_ctx=chat_ctx)
        await assistant.say(stream)

    @chat.on("message_received")
    def on_chat_received(msg: rtc.ChatMessage):
        if msg.message:
            asyncio.create_task(answer_from_text(msg.message))

    # Greet the user when the assistant starts
    await assistant.say("Hey, how can I assist you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))





















