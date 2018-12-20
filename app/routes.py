'''
flask-tweepy-oauth
an example showing how to authorize a twitter application
in python with flask and tweepy.
find the rest of the app here: https://github.com/whichlight/flask-tweepy-oauth
'''

import flask
from flask import request, render_template
from app import app
import tweepy

#config

CONSUMER_TOKEN='QxsBNX9XCiQpYqpRhnVPWQNu2'
CONSUMER_SECRET='2PbOTS5Gf9XWuMiRiuVIl1MENV2zYFKGz4WlI5oKxVk38NjfLA'
CALLBACK_URL = 'http://localhost:5000/verify'
session = dict()
db = dict() #you can save these values to a database

@app.route('/')
def home():
	user = {'username': 'Jessica'}
	return render_template('home.html', title='Jeschedule', user=user)

@app.route("/twitteroauth")
def send_token():
	auth = tweepy.OAuthHandler(CONSUMER_TOKEN,
		CONSUMER_SECRET,
		CALLBACK_URL)

	try:
		#get the request tokens
		redirect_url= auth.get_authorization_url()
		print('ok')
		session['request_token']= auth.request_token
		print('ok')
	except tweepy.TweepError:
		print('Error! Failed to get request token')

	#this is twitter's url for authentication
	return flask.redirect(redirect_url)

@app.route("/verify")
def get_verification():

	#get the verifier key from the request url
	verifier= request.args['oauth_verifier']
	print(request)
	print(verifier)
	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
	token = session.get('request_token')
	del session['request_token']

	auth.request_token = token

	try:
		    auth.get_access_token(verifier)
	except tweepy.TweepError:
		    print('Error! Failed to get access token.')

	#now you have access!
	api = tweepy.API(auth)

	#store in a db
	db['api']=api
	db['access_token_key']=auth.access_token
	db['access_token_secret']=auth.access_token_secret
	print('key: '+db['access_token_key'])
	print('secret: '+db['access_token_secret'])
	return flask.redirect(flask.url_for('start'))

@app.route("/start")
def start():
	#auth done, app logic can begin
	api = db['api']

	#example, print your latest status posts
	return flask.render_template('tweets.html', tweets=api.user_timeline())

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)

