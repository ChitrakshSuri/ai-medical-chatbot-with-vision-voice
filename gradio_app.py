# Voicebot UI with Gradio - Auto-Stop Version
import gradio as gr
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor_updated import tts_elevenlabs
import os
import tempfile

system_prompt = """
You are acting as a qualified medical doctor for educational purposes.

Carefully examine the image and the user's concern.
Based on what you observe, explain if there may be any medical issue and briefly suggest general remedies or next steps.

Important rules:
- Speak directly to the person, like a real doctor talking to a patient.
- Do NOT mention the image explicitly or say phrases like "in the image I see".
- Phrase your response as: "With what I see, I think you may have..."
- Do NOT use numbers, bullet points, emojis, markdown, or special characters.
- Do NOT say you are an AI or language model.
- Write in one clear, natural paragraph.
- Keep the response concise, maximum two sentences.
- Start immediately with the medical opinion, no introduction or preamble.
"""


def record_and_process(image_filepath, progress=gr.Progress()):
    """Records audio with auto-stop, then processes everything"""
    
    progress(0, desc="Preparing to record...")
    
    # Create temp file for audio
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    
    progress(0.1, desc="Recording... Speak now! (Auto-stops after 2s silence)")
    
    # Record with auto-stop
    record_audio(
        file_path=temp_audio,
        timeout=10,
        phrase_time_limit=30,
        pause_threshold=2.0  # Stops after 2 seconds of silence
    )
    
    progress(0.4, desc="Transcribing audio...")
    
    # Transcribe
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
        audio_filepath=temp_audio, 
        stt_model="whisper-large-v3"
    )

    progress(0.6, desc="Analyzing image...")
    
    # Analyze image
    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze"

    progress(0.8, desc="Generating doctor's voice...")
    
    # Generate voice
    voice_of_doctor = tts_elevenlabs(doctor_response)

    progress(1.0, desc="Complete!")

    return speech_to_text_output, doctor_response, voice_of_doctor, temp_audio


# Create interface with button-triggered recording
with gr.Blocks(title="AI Doctor with Vision and Voice") as iface:
    gr.Markdown("# 🏥 AI Doctor with Vision and Voice")
    gr.Markdown("""
    ### How to use:
    1. Upload a medical image (optional)
    2. Click **'🎤 Start Recording'** button
    3. **Speak your concern** (recording auto-stops after 2 seconds of silence)
    4. Get AI diagnosis and voice response
    """)
    
    with gr.Row():
        image_input = gr.Image(type='filepath', label="📸 Upload Medical Image (Optional)")
    
    record_btn = gr.Button("🎤 Start Recording & Analyze", variant="primary", size="lg")
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            transcription_output = gr.Textbox(label="📝 What You Said", lines=3)
            doctor_output = gr.Textbox(label="🩺 Doctor's Diagnosis", lines=5)
        with gr.Column():
            patient_audio = gr.Audio(label="🎤 Your Recording")
            doctor_audio = gr.Audio(label="🔊 Doctor's Voice Response")
    
    record_btn.click(
        fn=record_and_process,
        inputs=[image_input],
        outputs=[transcription_output, doctor_output, doctor_audio, patient_audio]
    )

iface.launch(debug=True, theme=gr.themes.Soft())