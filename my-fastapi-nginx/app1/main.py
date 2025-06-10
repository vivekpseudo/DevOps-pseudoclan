import whisper
import gradio as gr

print("== Loading model ==")
model = whisper.load_model("base")
print("== Model loaded ==")

def transcribe(audio_path):
    if audio_path is None:
        return "No audio received."

    try:
        print(f"== Received file: {audio_path} ==")
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)
        return result.text
    except Exception as e:
        return f"Transcription error: {str(e)}"

interface = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(type="filepath", label="🎤 Speak or Upload Audio"),  # ✅ FIXED: Removed `source`
    outputs=gr.Text(label="📝 Transcription"),
    live=True,
    title="🎙️ Whisper Speech-to-Text"
)

print("== Launching Interface ==")
interface.launch(server_name="0.0.0.0", server_port=7860)

