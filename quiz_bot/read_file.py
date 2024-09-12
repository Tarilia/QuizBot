import json


def read_file():
    with open('questions.json', 'r', encoding='utf-8') as file:
        quiz_data = json.load(file)
        return quiz_data
