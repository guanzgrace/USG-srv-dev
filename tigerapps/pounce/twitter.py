import tweepy

# TODO: fix this!  It's insecure.

consumerKey = "fMqSK9WSlqb0dpDiuijSg"
consumerSecret = "rrE5Z8z1BfXyJofAJuYvI4Tl4bIvIf0pkrV5FlPVg"

accessToken = "1213779152-RexnbcIOADAD5v6iVtl9DLSMtoLyaRlDcjJpxnO"
accessTokenSecret = "leTvvIf9FIGWJDVwhgFfPqoRrPHRuBONF0pwEGc6RY"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def tweet(message):
	api.update_status(message)