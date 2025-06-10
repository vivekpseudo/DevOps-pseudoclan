# Whisper Speech-to-Text App
This project is a simple and powerful speech-to-text web application powered by OpenAI's Whisper model and built using Gradio. It allows users to either record speech via a microphone or upload an audio file, transcribe the audio, and receive the recognized text output.

# Features
- Record audio via microphone or upload audio files.
- Get accurate transcriptions using the Whisper model.
- User-friendly Gradio web interface.
- Real-time processing with live transcription.

# Installation

1. Clone the Repository: 
*git clone
*cd whisper-speech-to-text

2. Install Dependencies
*pip install -r requirements.txt
*or manually: pip install openai-whisper gradio soundfile numpy

3. FFmpeg Installation Guide
*Whisper relies on ffmpeg for audio processing. Follow the steps below to install it:
*Download the latest static build from: https://www.gyan.dev/ffmpeg/builds/
*Extract to a folder (e.g., C:\ffmpeg).
*Add C:\ffmpeg\bin (bin folder's location that installed with ffmeg folder) to your system’s PATH environment variable.
-Confirm installation:
ffmpeg -version
ffprobe -version

4. Structure of the web app
- app.py: 	Main Python script to run the Gradio interface and handle speech transcription using Whisper.
- requirements.txt: Lists all Python dependencies required to run the application.
- readme.md: 	Documentation containing app description, setup instructions, and usage guide.
- .gradio/ (auto): Auto-generated folder used by Gradio to store logs and flagged inputs.

