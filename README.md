# AI-Powered Real-Time Chat Application

A real-time AI-powered chat application with audio support, built using Google's Gemini Live API and the Agent Development Kit (ADK). This project serves as a Chevrolet dealership assistant that can handle voice and text interactions with retrieval-augmented generation (RAG) for context-aware responses.

## Features

- **Real-Time Voice and Text Chat**: Bidirectional WebSocket communication for live interactions
- **AI Agent Integration**: Powered by Google's Gemini Live model for intelligent responses
- **Audio Processing**: Real-time audio recording and playback using Web Audio API
- **Retrieval-Augmented Generation (RAG)**: Context-aware responses using a SQLite database for dealership information
- **Web-Based UI**: Simple, responsive interface with chat logs and controls
- **Session Management**: Support for multiple user sessions with proper lifecycle handling

## Architecture

### Backend
- **main.py**: FastAPI WebSocket server handling real-time agent sessions
- **server/agent.py**: Defines the AI agent using Google's ADK with RAG context
- **server/rag.py**: Keyword-based retrieval system using SQLite database
- **server/prompt.py**: System prompt defining the AI's role as a dealership assistant
- **server/app.py**: Alternative Quart-based server (legacy)

### Frontend
- **client/index.html**: Main UI with chat interface and controls
- **client/main.js**: Core client logic for WebSocket, audio, and UI management
- **client/api-client.js**: WebSocket communication handler
- **client/audio-player.js** and **audio-recorder.js**: Audio processing worklets

### Data
- **retrieval_data.db**: SQLite database for RAG context
- **.env**: Environment variables for API keys and configuration

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js (for client-side development, optional)
- Google Cloud API key with access to Gemini Live

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Set up the virtual environment:
   ```
   python -m venv myenv
   myenv/Scripts/activate  # On Windows
   # source myenv/bin/activate  # On macOS/Linux
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   APP_NAME=your-app-name
   AGENT_VOICE=your-voice-name
   AGENT_LANGUAGE=en-US
   # Add your Google API key and other required variables
   ```

5. Initialize the database:
   ```
   # Run any setup scripts if available, or populate retrieval_data.db manually
   ```

### Running the Application
1. Start the server:
   ```
   python main.py
   ```
   The server will run on `http://localhost:8080` by default.

2. Open the client:
   Open `client/index.html` in a web browser.

3. Interact with the AI:
   - Click "Start Session" to begin
   - Use the microphone button for voice input
   - View real-time chat and logs

## Usage

- **Starting a Session**: Click the "Start Session" button to initiate a WebSocket connection and agent session.
- **Voice Input**: Use the microphone to send audio, which is transcribed and processed by the AI.
- **Text Input**: Send text messages directly via the WebSocket.
- **RAG Context**: The AI uses retrieval data from the database to provide informed responses about dealership services.

## Dependencies

### Python
- FastAPI
- Google's ADK and GenAI libraries
- Quart (legacy)
- gTTS (for audio synthesis)
- sqlite3
- python-dotenv

### JavaScript
- Web Audio API
- EventEmitter3
- Material Symbols (for UI icons)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational/demonstration purposes. Please check with the original authors for licensing information.

## Troubleshooting

- **Connection Issues**: Ensure the server is running and ports are not blocked.
- **Audio Problems**: Check browser permissions for microphone access.
- **API Errors**: Verify your Google API key and quotas.
- **Database Errors**: Ensure `retrieval_data.db` exists and is populated.

For more help, refer to the code comments or open an issue.
Note: The code is customised verison of Audio Bidirectional streaming in google ADK documentation: https://google.github.io/adk-docs/streaming/custom-streaming-ws/#next-steps-for-production



