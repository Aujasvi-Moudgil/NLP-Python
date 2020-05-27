

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import glob
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

senti = SentimentIntensityAnalyzer()

consumer_key = "buxCHFqoZQ3kTpgyl4gOucbUH"
consumer_secret = "fRbwf0lI8StJ39H4b3g512DCldgEUlpyoLHoEtvDaeQ1YVhNPY"

access_token = "2601458342-Al2CuzsD9lGyQIifKlqSZdowEswTYP4VawaX7O0"
access_token_secret = "HWyXCRHVeiF8ZIpPpysIP9CtvomCvRZE4hmvP6LefF2Ho"


def get_sentiment(text):
    score = senti.polarity_scores(text)['compound']
    if score > 0.05:
        return 'Positve'
    elif score < -0.05:
        return 'Negative'
    else:
        return 'Neutral'
       




class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        print('----Someone tweeted with #PulwamaAttack----')
        text = data['text']
        curr_tweet = {
        'text' : [data['text']],
        'created_at' : [data['created_at']],
        'retweets' : [data['retweet_count']],
        'likes' : [data['favorite_count']],
        'source' : [data['source']],
        'geo'  : [data['geo']],
        'profile_location' : [data['user']['location']],
        'profile_name': [data['user']['name']],
        'profile_description' : [data['user']['description']],
        'sentiment': [get_sentiment(data['text'])]
        }
        df_tweet = pd.DataFrame(curr_tweet)
        csv_file = 'tweets.csv'
        try:
            if csv_file in glob.glob('*csv'):
                #Append results
                with open(csv_file,'a') as f:                    #'a' is append
                    df_tweet.to_csv(f, header=False,index=False)
            else:
                #Create one and add data
                df_tweet.to_csv(csv_file,index=False)
        except:
            pass
                                          
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['#PulwamaAttack'])
    
 # Open command promt 
#cd to current day 3 folder 
# command: python twitter_streaming_api.py