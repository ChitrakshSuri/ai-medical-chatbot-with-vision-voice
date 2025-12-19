import os
import subprocess
import platform
from datetime import datetime
from gtts import gTTS
from elevenlabs import ElevenLabs

# -----------------------------
# Config
# -----------------------------
USE_ELEVENLABS = True #False top use gTTS
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# -----------------------------
# gTTS (fallback)
# -----------------------------
def tts_gtts(text: str) -> str:
    filename = f"gtts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    path = os.path.join(AUDIO_DIR, filename)

    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(path)

    return path


# -----------------------------
# ElevenLabs (NEW SDK)
# -----------------------------
def tts_elevenlabs(text: str) -> str:
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVEN_API_KEY not set")

    client = ElevenLabs(api_key=api_key)

    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # Aria
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    filename = f"elevenlabs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    path = os.path.join(AUDIO_DIR, filename)

    with open(path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    return path


# -----------------------------
# Audio playback (optional)
# -----------------------------
# def play_audio(filepath: str):
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":
#             subprocess.run(["afplay", filepath])
#         elif os_name == "Windows":
#             subprocess.run(
#                 ["powershell", "-c", f'(New-Object Media.SoundPlayer "{filepath}").PlaySync();']
#             )
#         elif os_name == "Linux":
#             subprocess.run(["aplay", filepath])
#     except Exception as e:
#         print("Playback error:", e)
def play_audio(filepath: str):
    import subprocess
    subprocess.run(["ffplay", "-autoexit", "-nodisp", filepath])


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    text = "Hi this is Chitraksh, your AI doctor speaking."

    if USE_ELEVENLABS:
        audio_path = tts_elevenlabs(text)
    else:
        audio_path = tts_gtts(text)

    print("Audio saved at:", audio_path)
    play_audio(audio_path)
