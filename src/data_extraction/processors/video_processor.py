import whisper
import os

def load_whisper_model(model_size="base"):
    print(f"--- Loading Whisper model ({model_size}) ---")
    return whisper.load_model(model_size)

def transcribe_video(video_path: str, model) -> str:
    try:
        result = model.transcribe(video_path)
        return f"SOURCE_FILE: {os.path.basename(video_path)}\n\n" + result['text']
    except Exception as e:
        return f"ERROR transcribing {video_path}: {e}"