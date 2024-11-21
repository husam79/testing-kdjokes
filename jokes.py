import json
from random import choice

def get_random_joke():
    jokes = []
    with open('jokes.json', 'r') as file:
        text = file.read()
        jokes = json.loads(text)

    return choice(jokes)['joke']