from flask import Flask, request, render_template
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    endpoint = os.environ['ENDPOINT']

    # Indicate that we want to translate ae
    query_parameter = '?q=' + original_text
    # Add the target language parameter
    target_language_parameter = '&langpair=en|' + target_language
    # Create the full URL
    constructed_url = endpoint + 'get' + query_parameter + target_language_parameter

    # Make the call using post
    translator_request = requests.get(constructed_url)
    # Retrieve the JSON response
    translator_response = translator_request.json()

    quota = not translator_response["quotaFinished"]
    if (quota):
        # Retrieve the translation
        translated_text = translator_response["responseData"]["translatedText"]

        # Call render template, passing the translated text,
        # original text, and target language to the template
        return render_template(
            'results.html',
            translated_text=translated_text,
            original_text=original_text,
            target_language=target_language
        )
    else:
        return '<p style="text-align:center;margin-top:45vh">🚅 Choo Choo 🚅<br />Your daily quota has finished!<br /> please try again tomorrow.</p>'


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
