# from barbershop.settings import MISTRAL_MODERATIOINS_GRADES
import os
from http.client import responses

from dotenv import load_dotenv
from mistralai import Mistral
from pprint import pprint

load_dotenv()

MISTRAL_MODERATIOINS_GRADES = {
    'hate_and_dicrimination' : 0.1,
    'sexual' : 0.1,
    'violence_and_threats' : 0.1,
    'dangerous_and_criminal_content' : 0.1,
    'selfharm' : 0.1,
    'health' : 0.1,
    'financial' : 0.1,
    'law' : 0.1,
    'pii' : 0.1,
}


MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

def is_bad_review(review_text, api_key = MISTRAL_API_KEY, grades = MISTRAL_MODERATIOINS_GRADES):

    client = Mistral(api_key = api_key)
    response = client.classifiers.moderate_chat(
        model = 'mistral-moderation-latest',
        inputs = [{'role':'user', 'content':review_text}],
    )

    result = response.results[0].category_scores

    result = {key:round(value, 2) for key, value in result.items()}

    pprint(result)

    checked_result = {}

    for key, value in result.items():
        if key in grades:
            checked_result[key] = value >= grades[key]

    return any(checked_result.values())

if __name__ == '__main__':
    print(is_bad_review(''))