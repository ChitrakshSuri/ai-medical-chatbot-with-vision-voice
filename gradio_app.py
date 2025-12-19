# Voicebot UI with Gradio
import gradio as gr
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor_updated import tts_elevenlabs, tts_gtts
import os

system_prompt = """
You are acting as a qualified medical doctor for educational purposes.

Carefully examine the image and the user’s concern.
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


def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get(
        "GROQ_API_KEY"), audio_filepath=audio_filepath, stt_model="whisper-large-v3")

    # handle the image input
    if image_filepath:
        doctor_reponse = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(
            image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct")
    else:
        doctor_reponse = "No image provided for me to analyze"

    voice_of_doctor = tts_elevenlabs(doctor_reponse)

    return speech_to_text_output, doctor_reponse, voice_of_doctor


# create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=['microphone'], type='filepath'),
        gr.Image(type='filepath')
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)
