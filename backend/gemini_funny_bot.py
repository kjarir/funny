# gemini_funny_bot.py
import requests
import json

API_KEY = "AIzaSyDKc3ZHVRa_q335956mUCwSBzYU3OJjGgo"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def get_funny_response(prompt):
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Tell this story in a very funny, silly tone for kids: {prompt}"
                    }
                ]
            }
        ]
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']
