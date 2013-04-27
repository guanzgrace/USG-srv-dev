import tweepy

# TODO: fix this!  It's insecure.

consumerKey = "fMqSK9WSlqb0dpDiuijSg"
consumerSecret = "rrE5Z8z1BfXyJofAJuYvI4Tl4bIvIf0pkrV5FlPVg"

accessToken = "1213779152-bzwOZQUrOd0vREdYDEEAbf9TUz0EbqhFzgBaHGP"
accessTokenSecret = "eWdiRW91lK3DqirM4K7ITddASUmtE8tbYoMHCz08"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

def tweet(message):
	api.update_status(message)