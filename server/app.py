import os
import re
import json
import base64
import asyncio
import tempfile
import websockets
from gtts import gTTS
from dotenv import load_dotenv

from root_agent.agent import root_agent

load_dotenv()
PORT = int(os.getenv("WS_PORT", 8765))

# ---------------- Text cleanup for TTS ----------------
def clean_for_tts(text: str) -> str:
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"-{2,}", " ", text)
    text = re.sub(r"[^\w\s.,!?']", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------------- TTS helper ----------------
def synthesize_audio(text: str) -> str:
    """Generate audio file (base64) from text."""
    tts = gTTS(text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        with open(fp.name, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
    return audio_b64

# ---------------- WebSocket Handler ----------------
async def handle_connection(websocket):
    # Send greeting
    await websocket.send(json.dumps({"event": "model_transcript", "data": "Hi! 👋 How can I help you today?"}))

    try:
        async for message in websocket:
            data = json.loads(message)
            event = data.get("event")

            if event == "user_transcript":  # client sent recognized text
                user_query = data.get("data", "")

                # Use Google ADK Agent for response
                response = await root_agent.run_async(user_query)
                reply = response.output_text

                # Prepare reply
                clean_reply = clean_for_tts(reply)
                audio_b64 = synthesize_audio(clean_reply)

                # Send back both transcript + audio
                await websocket.send(json.dumps({"event": "model_transcript", "data": reply}))
                await websocket.send(json.dumps({"event": "audio_chunk", "data": audio_b64}))
                await websocket.send(json.dumps({"event": "turn_complete"}))

            elif event == "end_session":
                await websocket.send(json.dumps({"event": "status", "data": "session_closed"}))
                break

    except websockets.exceptions.ConnectionClosedOK:
        print("🔌 Connection closed cleanly.")
    except Exception as e:
        print(f"❌ Error: {e}")

# ---------------- Main entry ----------------
async def main():
    print(f"🚀 WebSocket server running on ws://localhost:{PORT}")
    async with websockets.serve(handle_connection, "127.0.0.1", PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
