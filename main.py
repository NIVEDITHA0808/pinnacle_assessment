from dotenv import load_dotenv
import os
import json
import asyncio
import base64
import warnings
from pathlib import Path

from google.genai.types import Part, Content, Blob
from google.adk.runners import InMemoryRunner
from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from google.genai import types

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from google_search_agent.agent import root_agent

# Load Gemini API Key
load_dotenv()
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

APP_NAME = "Stevens Creek Chevrolet Assistant"

async def start_agent_session(user_id, is_audio=False):
    runner = InMemoryRunner(app_name=APP_NAME, agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=APP_NAME, user_id=user_id
    )
    modality = "AUDIO" if is_audio else "TEXT"
    run_config = RunConfig(
        response_modalities=[modality],
        session_resumption=types.SessionResumptionConfig()
    )
    live_request_queue = LiveRequestQueue()
    live_events = runner.run_live(
        session=session,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
    return live_events, live_request_queue


async def agent_to_client_messaging(websocket, live_events):
    try:
        async for event in live_events:
            if event.turn_complete or event.interrupted:
                message = {
                    "turn_complete": event.turn_complete,
                    "interrupted": event.interrupted,
                }
                await websocket.send_text(json.dumps(message))
                print(f"[AGENT TO CLIENT]: {message}")
                continue

            part: Part = (
                event.content and event.content.parts and event.content.parts[0]
            )
            if not part:
                continue

            if part.inline_data and part.inline_data.mime_type.startswith("audio/pcm"):
                audio_data = part.inline_data.data
                if audio_data:
                    message = {
                        "mime_type": "audio/pcm",
                        "data": base64.b64encode(audio_data).decode("ascii"),
                    }
                    await websocket.send_text(json.dumps(message))
                    print(f"[AGENT TO CLIENT]: audio/pcm {len(audio_data)} bytes")
                continue

            if part.text and event.partial:
                message = {"mime_type": "text/plain", "data": part.text}
                await websocket.send_text(json.dumps(message))
                print(f"[AGENT TO CLIENT]: text/plain: {message}")
    except WebSocketDisconnect:
        print("[AGENT TO CLIENT] Client disconnected")


async def client_to_agent_messaging(websocket, live_request_queue):
    try:
        while True:
            message_json = await websocket.receive_text()
            message = json.loads(message_json)
            mime_type = message["mime_type"]
            data = message["data"]

            if mime_type == "text/plain":
                content = Content(role="user", parts=[Part.from_text(text=data)])
                live_request_queue.send_content(content=content)
                print(f"[CLIENT TO AGENT]: {data}")
            elif mime_type == "audio/pcm":
                decoded_data = base64.b64decode(data)
                live_request_queue.send_realtime(
                    Blob(data=decoded_data, mime_type=mime_type)
                )
            else:
                print(f"[CLIENT TO AGENT] Unsupported mime type: {mime_type}")
    except WebSocketDisconnect as e:
        print(f"[CLIENT TO AGENT] Disconnected: code={e.code}, reason={e.reason}")


app = FastAPI()

STATIC_DIR = Path("static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, is_audio: str):
    await websocket.accept()
    print(f"Client #{user_id} connected, audio mode={is_audio}")

    live_events, live_request_queue = await start_agent_session(
        str(user_id), is_audio == "true"
    )

    agent_to_client_task = asyncio.create_task(
        agent_to_client_messaging(websocket, live_events)
    )
    client_to_agent_task = asyncio.create_task(
        client_to_agent_messaging(websocket, live_request_queue)
    )

    try:
        await asyncio.wait(
            [agent_to_client_task, client_to_agent_task],
            return_when=asyncio.FIRST_EXCEPTION,
        )
    except asyncio.CancelledError:
        print(f"Client #{user_id} tasks cancelled (shutdown)")
    finally:
        live_request_queue.close()
        print(f"Client #{user_id} disconnected and cleaned up")
