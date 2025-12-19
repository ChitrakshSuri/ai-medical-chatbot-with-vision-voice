# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


input_text="Hi this is Chitraksh!"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import os
from datetime import datetime
from elevenlabs import ElevenLabs

def text_to_speech_with_elevenlabs_old(
    input_text: str,
    output_dir: str = "audio",
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",  # Aria
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128"
):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set")

    client = ElevenLabs(api_key=api_key)

    audio_stream = client.text_to_speech.convert(
        text=input_text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format
    )

    os.makedirs(output_dir, exist_ok=True)
    filename = f"elevenlabs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    return filepath


if __name__ == "__main__":
    path = text_to_speech_with_elevenlabs_old(
        "Hi this is Chitraksh, your AI doctor speaking."
    )
    print("Saved to:", path)

#Step2: Use Model for Text output to Voice

import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


input_text="Hi this is Chitraksh, autoplay testing!"
text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


def text_to_speech_with_elevenlabs(
    input_text: str,
    output_dir: str = "audio",
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",  # Aria
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128"
):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set")

    client = ElevenLabs(api_key=api_key)

    audio_stream = client.text_to_speech.convert(
        text=input_text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format
    )

    os.makedirs(output_dir, exist_ok=True)
    filename = f"elevenlabs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    return filepath


#text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")