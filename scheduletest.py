import schedule
import tweepy
import time
import argparse

def twitter_connection():
	CONSUMER_TOKEN='QxsBNX9XCiQpYqpRhnVPWQNu2'
	CONSUMER_SECRET='3PbOTS5Gf9XWuMiRiuVIl1MENV2zYFKGz4WlI5oKxVk38NjfLA' #2
	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
	auth.set_access_token('4149279015-3PxStqBNBP9qHnmmNn4A4TWYxA0wv7eEkAJJeHt','NXpfF3mO0CLW2CqlPY4fXzwqhWPoWGSBkRDoMLqTIqIvw')#NZ
	api = tweepy.API(auth)
	return api

def send_tweet(text):
	api = twitter_connection()
	api.update_status(text)
	exit()

def schedule_tweet(hour, minute, text):
	schedule.every().day.at(str(hour)+':'+str(minute)).do(send_tweet(text))

	while True:
		schedule.run_pending()
		time.sleep(1)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-w", "--hour", help="hour at the time to send the tweet", type=int)
	parser.add_argument("-m", "--minute", help="minute at the time to send the tweet", type=int)
	parser.add_argument("-t", "--text", help="text to tweet", type=str)
	args = parser.parse_args()
	schedule_tweet(args.hour, args.minute, args.text)
