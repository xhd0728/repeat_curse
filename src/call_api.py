import requests
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), '../config/.env')
load_dotenv(env_path)


def get_gemini(prompt):
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": google_api_key
    }
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt}
            ]
        }],
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ],
        "generationConfig": {
            "stopSequences": [
                "Title"
            ],
            "temperature": 1.0,
            "maxOutputTokens": 800,
            "topP": 0.8,
            "topK": 10
        }
    }
    res = requests.post(url, headers=headers, params=params, json=payload)
    return res.json()["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == '__main__':
    get_gemini("hello")
