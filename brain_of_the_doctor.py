# Step 1: Setup GROQ API Key
from groq import Groq
import base64
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Step 2: Convert image to required format
image_path = 'acne.jpg'
image_file = open(image_path, "rb")  # read binary
encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Step 3: Setup Multimodal LLM

client = Groq()
query = "is there something wrong with my face?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            }
        ]
    }
]

chat_completion = client.chat.completions.create(
    messages=messages,
    model=model
)

print(chat_completion)