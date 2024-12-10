import os
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq
from functions.database import get_recent_messages
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def convert_audio_to_text(audio_file):
    try:
        response = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
        return response.text
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return None


def get_chatResponse(message_input):
    messages = get_recent_messages()
    # messages = []
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)
    print(messages)
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model='Llama-3.3-70B-versatile'
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting chat response: {str(e)}")
        return None
