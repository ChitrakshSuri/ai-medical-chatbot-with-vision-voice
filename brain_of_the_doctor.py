# Step 1: Setup GROQ API Key
import os
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

# Step 2: Convert image to required format
import base64
image_path='acne.jpg'
image_file=open(image_path, "rb") #read binary
encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Step 3: Setup Multimodal LLM