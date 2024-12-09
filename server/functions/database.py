import json
import random
import os


def get_recent_messages():
    """Get recent messages from a JSON file"""
    messages = []
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the JSON file
    file_path = os.path.join(current_dir, "..", "stored_data.json")
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
    return messages


"""     try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    # recent_messages = sorted(data, key=lambda x: x['timestamp'], reverse=True)
                    for item in data[-5:]:
                        messages.append(item)

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        pass """
