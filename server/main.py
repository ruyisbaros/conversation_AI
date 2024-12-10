import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from fastapi.responses import StreamingResponse
from groq import Groq
from functions.openai_request import convert_audio_to_text, get_chatResponse
from functions.database import store_message, reset_messages
load_dotenv()

app = FastAPI()


# CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:4173",
        "http://localhost:3000",
        "http://localhost:4174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

""" chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of low latency LLMs",
        }
    ],
    model="llama3-8b-8192",
)
print(chat_completion.choices[0].message.content) """


@app.get("/health")
async def check_health():
    return {"message": "Healthy"}


@app.get("/get_audio")
async def get_audio():
    print("Getting audio")
    audio_input = open("Voice001.wav", "rb")
    print("Decoding audio")
    converted_audio = convert_audio_to_text(
        audio_input)  # convert audio to text Whisper
    print("Transcribed audio:", converted_audio)
    # return StreamingResponse(converted_audio, media_type="audio/wav")
    if not converted_audio:
        raise HTTPException(
            status_code=400, detail="Failed to transcribe audio")
    # get chat response from Groq
    ai_response = get_chatResponse(converted_audio)
    if not ai_response:
        raise HTTPException(
            status_code=400, detail="Failed to response from server")

    # Store the response
    store_message(request_message=converted_audio,
                  response_message=ai_response)
    print("AI response:", ai_response)
    # return {"transcription": converted_audio}  # for testing purposes, replace with groq response
    return {"transcription": ai_response}


@app.get("/reset")
async def reset_m():
    reset_messages()
    return {"message": "Messages reset"}
