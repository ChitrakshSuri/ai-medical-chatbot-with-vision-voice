import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=10, phrase_time_limit=None, energy_threshold=300, pause_threshold=2.0):
    """
    Record audio with automatic silence detection.
    
    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Maximum time to wait for speech to start (in seconds).
        phrase_time_limit (int): Maximum duration of recording (in seconds). None for unlimited.
        energy_threshold (int): Microphone sensitivity (lower = more sensitive). Default 300.
        pause_threshold (float): Seconds of silence to stop recording. Default 2.0.
    """
    recognizer = sr.Recognizer()
    
    # Configure for better automatic stopping
    recognizer.energy_threshold = energy_threshold  # Adjust sensitivity
    recognizer.pause_threshold = pause_threshold    # Silence duration before stopping
    recognizer.dynamic_energy_threshold = True      # Auto-adjust to ambient noise
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise... (1 second)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info(f"Ready! Start speaking... (Will auto-stop after {pause_threshold}s of silence)")
            
            # Record with automatic silence detection
            audio_data = recognizer.listen(
                source, 
                timeout=timeout, 
                phrase_time_limit=phrase_time_limit
            )
            logging.info("Recording complete - silence detected.")
            
            # Convert to MP3
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")
            
    except sr.WaitTimeoutError:
        logging.error(f"No speech detected within {timeout} seconds")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# ADD THIS FUNCTION:
def transcribe_with_groq(GROQ_API_KEY, audio_filepath, stt_model):
    """
    Transcribe audio file using Groq's Whisper model.
    
    Args:
        GROQ_API_KEY (str): Groq API key
        audio_filepath (str): Path to audio file
        stt_model (str): Model name for transcription
        
    Returns:
        str: Transcribed text
    """
    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )

    return transcription.text


# Test function
if __name__ == "__main__":
    audio_filepath = "patient_voice_test_auto.mp3"
    
    # Test recording
    record_audio(
        file_path=audio_filepath,
        timeout=10,              # Wait 10s for speech to start
        phrase_time_limit=30,    # Max 30s recording
        energy_threshold=300,    # Mic sensitivity (adjust if needed)
        pause_threshold=1.5      # Stop after 1.5s of silence
    )
    
    # Test transcription
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    text = transcribe_with_groq(
        GROQ_API_KEY=GROQ_API_KEY,
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )
    print(f"Transcription: {text}")