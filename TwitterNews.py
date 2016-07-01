import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import configparser


def loadtwitterinfo():
    cfg = configparser.ConfigParser()
    cfg.read('twitterinfo.ini')

    info = {}
    options = cfg.options('Twitter Info')
    for option in options:
        try:
            info[option] = cfg.get('Twitter Info', option)
        except KeyError:
            info[option] = None
    return info

twitterInfo = loadtwitterinfo()


class Listener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(twitterInfo['consumer_key'], twitterInfo['consumer_secret'])
auth.set_access_token(twitterInfo['access_token'], twitterInfo['access_secret'])

api = tweepy.API(auth)
print(api.user_timeline('NBAcom')[0].text)
# twitterStream = Stream(auth, Listener())
# twitterStream.filter(track=["nba"])

