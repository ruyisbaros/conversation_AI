import os
from openai import OpenAI
from logging import logger

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


async def generate_speech(text: str):
    """Generate speech using OpenAI TTS"""
    try:
        response = await openai_client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        # Get the speech data directly from the response
        # No need to await response.read() as the response is already the audio data
        return response.content
    except Exception as e:
        logger.error(f"Speech generation error: {str(e)}")
        return None
