# Stevens Creek Chevrolet Voice Assistant

A real-time streaming voice assistant for Stevens Creek Chevrolet dealership built with Google's Agent Development Kit (ADK), FastAPI, and WebSockets.

## Overview

This application demonstrates a conversational AI assistant that can handle both text and audio interactions. The assistant, named "Stevy", provides information about vehicle sales specials, service offers, EV incentives, and vehicle inventory by scraping real-time data from the dealership's website.

## Features

- **Real-time Streaming**: Supports both text and audio modalities for natural conversation
- **WebSocket Communication**: Bidirectional real-time communication between client and server
- **Tool Integration**: Uses custom tools to fetch live data from stevenscreekchevy.com
- **Audio Processing**: Records and plays back audio using Web Audio API
- **Session Management**: Maintains conversation context per user session

## Architecture

### Backend (FastAPI)
- **main.py**: FastAPI server with WebSocket endpoint `/ws/{user_id}`
- **Agent**: Powered by Google's Gemini 2.0 Flash Live model
- **Tools**: Web scraping tools for dealership data
- **Session Handling**: Uses ADK's InMemoryRunner for live agent sessions

### Frontend
- **index.html**: Simple web interface with chat display and input controls
- **app.js**: WebSocket client with audio recording/playback capabilities
- **Audio Worklets**: Custom audio processing for real-time streaming

### Agent Components
- **voice_agent/agent.py**: Agent definition with model and tools
- **voice_agent/prompt.py**: System instructions for the assistant's behavior
- **voice_agent/tools/tools.py**: Web scraping tools using BeautifulSoup
```
             ┌───────────────────────────┐
             │   Microphone (User voice) │
             └───────────────┬───────────┘
                             │ getUserMedia()
                             ▼
                   MediaStreamSource (WebAudio)
                             │
                             ▼
┌─────────────────────────────┴───────────────────────────────┐
│ Recorder Worklet (pcm-recorder-processor.js)                 │
│ - Captures Float32 mic samples                               │
│ - Sends to main thread                                       │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
         convertFloat32ToPCM() → Int16 PCM
                             │
                             ▼
          ┌───────────────────────────────────┐
          │   WebSocket / API → Voice Agent   │
          │   (Gemini / OpenAI / Custom)      │
          │                                   │
          │ Agent Pipeline:                   │
          │  1. Speech-to-Text (STT)          │
          │  2. Pass text to LLM Agent        │
          │     - SYSTEM_PROMPT               │
          │     - Tools (get_sales_specials,  │
          │       get_service_content, etc.)  │
          │  3. Agent generates text response │
          │  4. Text-to-Speech (TTS)          │
          └───────────────────────────────────┘
                             │
             Agent response PCM (Int16)
                             │
                             ▼
┌─────────────────────────────┴───────────────────────────────┐
│ Player Worklet (pcm-player-processor.js)                     │
│ - Receives PCM chunks from agent                             │
│ - Buffers in ring buffer                                     │
│ - Converts to Float32                                        │
│ - Streams out to speakers                                    │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
                        🔊 Speakers
```
## Prerequisites

- Python 3.11+
- Google Cloud API key with access to Gemini models
- Internet connection for web scraping

## Setup

1. **Clone the repository** (if applicable) and navigate to the app directory:
   ```bash
   git clone https://github.com/NIVEDITHA0808/pinnacle_assessment.git
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   - Copy `.env` and set your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

4. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Open in browser**:
   - Navigate to `http://localhost:8000`
   - Click "🎤 Start Audio" to enable voice mode
   - Type messages or speak to interact with the assistant

## Usage

### Text Mode
- Type messages in the input field and press Send
- The assistant will respond with text in real-time

### Audio Mode
- Click "🎤 Start Audio" to enable microphone access
- Speak naturally - audio is streamed in 200ms chunks
- Responses are played back through the browser

### Available Tools
The assistant can provide information on:
- Sales specials and promotions
- Service specials and offers
- EV purchase incentives
- Electric vehicle inventory
- Gas vehicle inventory
- Service department information

## Configuration

- **Model**: Configured to use `gemini-2.0-flash-live-001`
- **Audio Format**: PCM audio at 16kHz
- **Web Scraping**: Targets specific pages on stevenscreekchevy.com
- **Session Timeout**: Automatic cleanup on WebSocket disconnect

## Development

### Project Structure
```
app/
├── main.py                 # FastAPI server
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── voice_agent/
│   ├── agent.py           # Agent definition
│   ├── prompt.py          # System prompt
│   └── tools/
│       ├── tools.py       # Scraping tools
│       └── utils.py       # Helper functions
└── static/
    ├── index.html         # Web interface
    └── js/
        ├── app.js         # Main client script
        ├── audio-player.js # Audio playback worklet
        └── audio-recorder.js # Audio recording worklet
```

### Adding New Tools
1. Define the tool function in `tools/tools.py`
2. Decorate with `@function_tool`
3. Add to the agent's tools list in `agent.py`
4. Update the system prompt in `prompt.py`

### Customizing the Assistant
- Modify the system prompt in `prompt.py` to change behavior
- Update scraping URLs in `tools/tools.py` for different dealerships
- Adjust audio parameters in the client JavaScript

## Troubleshooting

- **WebSocket Connection Issues**: Check that the server is running on port 8000
- **Audio Not Working**: Ensure microphone permissions are granted in browser
- **Tool Errors**: Verify internet connection for web scraping
- **API Errors**: Confirm Google API key is valid and has proper permissions

## License

Copyright 2025 Google LLC. Licensed under the Apache License, Version 2.0.


