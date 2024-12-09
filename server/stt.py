import wave
import os
from groq import Groq

groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))


async def transcribe_audio(audio_data: bytes):
    """Transcribe audio using Groq's Whisper model"""
    temp_wav = None
    try:
        # Create a unique temporary file
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        wav_path = temp_wav.name
        temp_wav.close()  # Close the file handle immediately

        # Write the WAV file
        with wave.open(wav_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wav_file.setframerate(16000)  # 16kHz
            wav_file.writeframes(audio_data)

        # Transcribe using Groq
        with open(wav_path, 'rb') as audio_file:
            response = await groq_client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=audio_file,
                response_format="text"
            )
    finally:
        # Delete the temporary file
        if temp_wav:
            os.remove(temp_wav.name)
        return response
