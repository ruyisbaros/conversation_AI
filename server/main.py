import os
from dotenv import load_dotenv
from fastapi import FastAPI  # type: ignore
from groq import Groq

load_dotenv()

app = FastAPI()


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


@app.get("/")
async def read_file():
    print("Reading file")
    return "Hello, worldddddd!"
