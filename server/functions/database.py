import json
import random
import os


def get_recent_messages():
    """Get recent messages from a JSON file"""
    messages = []
    file_path = 'stored_data.json'
    # Define prompt
    learn_instruction = {
        "role": "system",
        "content": "Your name is Rachel. The user name is Ahmet. You are interviewing the user for a job as retail assistant.\
        Ask short questions that are relevant to the junior position. Keep your answers max 30 words!",
    }

    x = random.uniform(0, 1)

    if x < 0.5:
        learn_instruction["content"] += " Your response will include some dry humour."
    else:
        learn_instruction["content"] += " Your response will include rather challenging question."

    messages.append(learn_instruction)

    try:
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                if data:
                    if len(data) < 5:
                        for item in data:
                            messages.append(item)
                    else:
                        # recent_messages = sorted(data, key=lambda x: x['timestamp'], reverse=True)
                        for item in data[-5:]:
                            messages.append(item)
            except Exception as e:
                print(f"Error loading JSON data: {str(e)}")
                pass

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        pass

    return messages


def store_message(request_message, response_message):
    file_path = 'stored_data.json'

    messages = get_recent_messages()[1:]  # exclude system messages

    user_messages = {
        "role": "user",
        "content": request_message,
    }

    bot_messages = {
        "role": "assistant",
        "content": response_message,
    }
    messages.append(user_messages)
    messages.append(bot_messages)

    try:
        with open(file_path, 'w') as file:
            json.dump(messages, file, indent=2)
    except Exception as e:
        print(f"Error storing JSON data: {str(e)}")


def reset_messages():
    file_path = 'stored_data.json'

    try:
        with open(file_path, 'w') as file:
            json.dump([], file, indent=2)
    except Exception as e:
        print(f"Error resetting JSON data: {str(e)}")
