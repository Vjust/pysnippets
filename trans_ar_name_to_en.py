"""
Translate Arabic strings to English, using
Google Translate API

Note : Setup a Google API Key. Its required for this code to work.

Other dependencies (add via Pip-install) :
google-api-python-client
python-gflags
"""
import os

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
from apiclient.discovery import build
service = build('translate', 'v2', developerKey=GOOGLE_API_KEY)


def trans_ar_name_to_en(name_string):
    """ Accepts an arabic string to english """
    res = service.translations().list(
        source='ar',
        target='en',
        q=[name_string]).execute()
    out = res['translations'][0]['translatedText']
    return out
