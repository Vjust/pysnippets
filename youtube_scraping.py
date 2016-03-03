"""
  Youtube MetaData api.
  Uses GOOGLE_API_KEY.

  Usage : get_channel('bbc')
"""

import os
import urllib
import requests
import json

channel_list = open('youtube/old_channel_list.txt').readlines()
api_url = "https://www.googleapis.com/youtube/v3/"


def lookup_channel(channel_name):
    """ Lookup a channel,
    Return Public Y/N ,status:Public/Private (for the first)"""
    furl = get_channel_url(channel_name)
    r = requests.get(furl)
    if r.status_code != 200:
        return r.status_code, 0, ""
    try:
        resp_data = json.loads(r.content)
        totalResults = resp_data['pageInfo']['totalResults']
        privacy_status = resp_data['items'][0]['status']['privacyStatus']
        return r.status_code, totalResults, privacy_status
    except:
        print resp_data
        return r.status_code, 0, ""


def get_channel_url(search_string, part='status'):
    """ Form a URL.  part is by default using status and content details"""
    query_args = {'part': part,
                  'forUsername': search_string,
                  'key': os.getenv('GOOGLE_API_KEY')
                  }
    encoded_args = urllib.urlencode(query_args)
    print api_url + "channels?" + encoded_args
    return api_url + "channels?" + encoded_args
