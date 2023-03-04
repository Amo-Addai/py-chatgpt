import subprocess
import requests
import json
import os
import readline  # optional, for better command line input experience
import whisper

api_url = 'https://api.openai.com/v1'
w_api_url = 'https://whisper.lablab.ai'

# define function to generate text from speech
def generate_text_from_speech(filepath='{}/data/audio.mp3'.format(os.getcwd())):
    # print(filepath)
    # subprocess.call(["afplay", filepath]) # confirms audio file
    model = whisper.load_model("base")
    response = model.transcribe(filepath)
    print(response)
    if 'text' in response: return response['text'].strip()
    else: return ''

# define function to generate response
def generate_response(prompt):
    headers = {
        'Authorization': 'Bearer {0}'.format(os.getenv('OPENAI_API_KEY')),
        'Content-Type': 'application/json',
    }
    body = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 7,
        "temperature": 0
    }
    data = json.dumps(body)
    # print({ 'headers': headers, 'body': data })
    response = requests.post('{}/completions'.format(api_url), headers=headers, data=data)
    response = response.json()
    return response['choices'][0]['text'].strip()


user_input = '{}/data/audio.mp3'.format(os.getcwd())
# NOTE: user can also be asked for an audio input stream
text = generate_text_from_speech(user_input)
print('Audio Speech: {}'.format(text))
prompt = f"{text}\nA:"

# main loop to receive user input and generate response
while True:
    response = generate_response(prompt)
    print(">> {}".format(response))
    user_input = input("> ")
    prompt = f"{user_input}\nA:"
