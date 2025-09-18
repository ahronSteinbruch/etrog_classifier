#!/usr/bin/env python3

import base64
from openai import OpenAI

with open("prompt.txt", "r") as p:
    prompt = p.read()


def encode_image(image_path):
    """Encode image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_lmstudio_chat():
    # Configure OpenAI client to point to LM Studio
    client = OpenAI(
        base_url="https://lm-tunnel.null-force.org/v1",
        api_key="lm-studio"  # LM Studio doesn't require a real API key
    )

    try:
        print("Sending request to LM Studio using OpenAI library...")
        print("Model: google/gemma-3-4b")
        print("Message: Hello! Can you tell me what model you are and confirm you're working properly?")
        print("-" * 50)

        completion = client.chat.completions.create(
            model="google/gemma-3-4b",
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Can you tell me what model you are and confirm you're working properly?"
                }
            ],
            temperature=0.7,  # Controls randomness (0.0-1.0)
            max_tokens=500    # Maximum response length
        )

        assistant_message = completion.choices[0].message.content
        print("Response from model:")
        print(assistant_message)
        print("-" * 50)
        print(f"Usage: {completion.usage.prompt_tokens} prompt tokens, {completion.usage.completion_tokens} completion tokens")
        print("✅ Test successful! LM Studio is handling OpenAI library requests properly.")

    except Exception as e:
        print(f"❌ Error: {e}")

def test_lmstudio_vision():
    """Test LM Studio with image input"""
    client = OpenAI(
        base_url="https://lm-tunnel.null-force.org/v1",
        api_key="lm-studio"
    )

    try:
        print("Testing image processing with LM Studio...")
        print("Image: image.png")
        print("-" * 50)
        image_path = ""
        # Encode the image
        base64_image = encode_image(image_path)

        completion = client.chat.completions.create(
            model="google/gemma-3-27b",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.2,  # Controls randomness (0.0-1.0)
            max_tokens=1000    # Maximum response length
        )

        assistant_message = completion.choices[0].message.content
        print("Response from model:")
        print(assistant_message)
        print("-" * 50)
        print(f"Usage: {completion.usage.prompt_tokens} prompt tokens, {completion.usage.completion_tokens} completion tokens")
        print("✅ Vision test successful!")

    except Exception as e:
        print(f"❌ Vision test error: {e}")

if __name__ == "__main__":
    # print("Testing LM Studio with text...")
    # test_lmstudio_chat()
    # print("\n" + "="*60 + "\n")
    print("Testing LM Studio with image...")
    test_lmstudio_vision()