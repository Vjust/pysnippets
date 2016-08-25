"""
An implementation of Twitter Oauth Pin based authentication
Stores Twitter access tokens in a config file,
for re-use (until Twitter expires them)

All credentials are read (and written back to) a config file

Thanks to :

Stack Overflow 
  http://stackoverflow.com/questions/16078366/reuse-oauth1-authorization-tokens-with-rauth

Note : Make sure config secrets are in gitignore / encrypted
"""

from rauth.service import OAuth1Service
import os
import configparser


class TwitterClient:

    user = None
    config = None

    def __init__(self):

        if self.config is None:
            self.config = configparser.ConfigParser()
            self.config.read('config_secret.ini')
            self.user = self.config.get('provider', 'user')
        self.twitter = OAuth1Service(
            name='twitter',
            consumer_key=self.config.get('provider', 'consumer_key'),
            consumer_secret=self.config.get('provider', 'consumer_secret'),
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            base_url='https://api.twitter.com/1.1/')

    def new_session(self):
        request_token, request_token_secret = self.twitter.get_request_token()
        authorize_url = self.twitter.get_authorize_url(request_token)
        print 'Visit this URL in your browser: ' + authorize_url
        pin = raw_input('Enter PIN from browser: ')
        session = self.twitter.get_auth_session(request_token,
                                                request_token_secret,
                                                method='POST',
                                                data={'oauth_verifier': pin})
        # write access tokens to secret file
        f = open("config_secret.ini", 'w')
        self.config.set('provider', 'access_token', session.access_token)
        self.config.set('provider', 'access_token_secret', session.access_token_secret)
        self.config.write(f)
        f.close()
        return session

    def reuse_session(self):
        access_token = self.config.get('provider','access_token')
        access_token_secret = self.config.get('provider', 'access_token_secret')
        session = self.twitter.get_session((access_token, access_token_secret))
        return session

    def init_session(self, user):
        # these two options should always be there, they dont change
        if not self.config.has_option('provider', 'consumer_key') or \
           not self.config.has_option("provider", 'user'):
            raise Exception("No session credentials, check config")

        if not self.config.has_option('provider', 'access_token'):
            self.user = user
            session = self.new_session()
        else:
            session = self.reuse_session()

        return session

    def list_tweets(self, user):
        try:
            session = self.init_session(user)
            params = {'include_rts': 1,  # Include retweets
                      'count': 10}       # 10 tweets

            r = session.get('statuses/home_timeline.json', params=params)

            for i, tweet in enumerate(r.json(), 1):
                handle = tweet['user']['screen_name'].encode('utf-8')
                text = tweet['text'].encode('utf-8')
                print '{0}. @{1} - {2}'.format(i, handle, text)
        except:
            pass


tc = TwitterClient()
tc.list_tweets(tc.user)
