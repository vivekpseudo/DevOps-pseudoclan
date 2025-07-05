from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import argostranslate.translate
from gtts import gTTS
import whisper, gradio as gr
import os, uuid

app = FastAPI()

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load translation models
argostranslate.translate.load_installed_languages()

# Load Whisper model
model = whisper.load_model("base")

# === Text-to-Speech Endpoint ===
@app.post("/text-to-speech/")
async def text_to_speech(
    text: str = Form(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...)
):
    installed_languages = argostranslate.translate.get_installed_languages()

    from_lang = next((lang for lang in installed_languages if lang.code == source_lang), None)
    to_lang = next((lang for lang in installed_languages if lang.code == target_lang), None)

    if not from_lang or not to_lang:
        return {"error": "Language not installed"}

    translation = from_lang.get_translation(to_lang)
    translated_text = translation.translate(text)

    tts = gTTS(text=translated_text, lang=target_lang)
    os.makedirs("audio", exist_ok=True)
    filename = f"audio/{uuid.uuid4()}.mp3"
    tts.save(filename)

    return FileResponse(filename, media_type="audio/mpeg", filename="speech.mp3")

@app.get("/")
def home():
    return {"message": "FastAPI app with both Text-to-Speech and Speech-to-Text"}

# === Gradio Speech-to-Text UI ===
def transcribe(audio_path):
    if audio_path is None:
        return "No audio received."

    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text

gradio_app = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(type="filepath", label="🎤 Speak or Upload Audio"),
    outputs=gr.Text(label="📝 Transcription"),
    title="🎙️ Whisper Speech-to-Text"
)

# Mount Gradio inside FastAPI at `/speech-to-text`
from fastapi.middleware.wsgi import WSGIMiddleware
app.mount("/speech-to-text", WSGIMiddleware(gradio_app.launch(inline=False)))
