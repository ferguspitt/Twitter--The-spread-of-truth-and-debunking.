
''' 
!!! This is an experiment for University Homework. Not ready to be used in production. Real conclusions should not be drawn.

I'm publishing it now in the hope of getting feedback on the process, code and ideas.
 Cheers, 
 Fergus Pitt


Question: What happened with various entities' reports of various news stories about the suspects in Boston Bombing?


- What was the difference in attention between assertion and corrections?
- What was the difference in attention between different entities' statements of the same story?

- Measures of attention for tweets: Retweets, Replies, (These can be either in absolute, or relative to the number of followers)
- Measures of attention for URLs (NOT YET IMPLEMENTED): Links from twitter; bit.ly link metrics

Relevant Ontology of a tweet: Time, AccountHolder (CLASSIFICATION By Brand, Reporter, Govt, SubBrand/Program, Unaffiliated Citizen NOT YET IMPLEMENTED), Number of Replies, Number of RTs, Number of Favorites, content, 
Relevant Ontology of a story: News Event, Attribution (Official, Other Media, Own Sources, Statement), Type (Assertion, Clarification, Retraction, Debunking), Accuracy

Notes: The Ontology of the story will be entered manually, because I think it needs human intelligence. The attribution might want more refining: Should there be differentiation between named, unnamed and official sources?

'''

from urllib import urlopen
from json import loads
from bs4 import BeautifulSoup
import re
from __future__ import division
import datetime

'''Input tweet & Analyse: Function need inputs of URL, Asks for News Event, Attribution and Type


Get tweet, Get Number of RTs, Get Number of Replies, Get AccountHolder, Get Number of followers, 
Return a dictionary with Variables above and RTs/Followers, Replies/Followers 


'''


#def TweetInput(User,TweetID):
def TweetInput(TweetURL):
	
	output={}
	#Make all the URLs and IDs we need
	UserMatch=re.search(r'https://twitter.com/[a-zA-Z_-]+',TweetURL)
	if UserMatch:
		User=UserMatch.group(0)
		User=User.replace('https://twitter.com/','')

	TweetIDMatch=re.search(r'statuses/[0-9]+',TweetURL)
	if TweetIDMatch:
		TweetID=TweetIDMatch.group(0)
		TweetID=TweetID.replace('statuses/','')
	TweetIDMatch=re.search(r'status/[0-9]+',TweetURL)
	if TweetIDMatch:
		TweetID=TweetIDMatch.group(0)
		TweetID=TweetID.replace('status/','')

	AccountURL="https://twitter.com/"+User
	jsonURL="https://api.twitter.com/1/statuses/oembed.json?id="+TweetID
	#Start Getting the numbers, First the number of RTs
	data=urlopen(TweetURL).read()
	match=re.search(r'<strong>.+</strong> Retweets',data)
	if match:
		retweets=match.group(0)
		retweets=retweets.replace('<strong>','')
		retweets=retweets.replace('</strong> Retweets','')
		retweets=int(retweets.replace(',',''))
	else:
		retweets=0
	#Now get the number of times favorited
	match2=re.search(r'<strong>.+</strong> Favorites',data)
	if match2:
		favorites=match2.group(0)
		favorites=favorites.replace('<strong>','')
		favorites=favorites.replace('</strong> Favorites','')
		favorites=int(favorites.replace(',',''))
	else:
		favorites=0	
	#Now start getting the number of followes (Note, at run time, not the time of tweet!!)
	AccountData=urlopen(AccountURL).read()
	match3=re.search(r'<strong>.+</strong> Followers',AccountData)
	if match3:
		followers=match3.group(0)
		followers=followers.replace('<strong>','')
		followers=followers.replace('</strong> Followers','')
		followers=int(followers.replace(',',''))
	else:
		followers=0
	retweetsPerFollower=retweets/followers
	favoritesPerFollower=favorites/followers
	#Get the content of the tweet for readability of results
	jsonData=loads(urlopen(jsonURL).read())
	html=str(jsonData['html'])
	soup=BeautifulSoup(html)
	content=''
	for string in soup.p.strings:
		content=content+str(string)
	match4=re.search(r'data-time="[0-9]+"',data)
	if match4:
		twittimeStamp=match4.group(0)
		twittimeStamp=twittimeStamp.replace('data-time="','')
		twittimeStamp=twittimeStamp.replace('"','')
		twittimeStamp=datetime.datetime.fromtimestamp(int(twittimeStamp)).strftime('%Y-%m-%d %H:%M:%S')
	else:
		twittimeStamp='UnKnown'

	#Get the user's help.
	print("\n\n\nI need you to help me by telling me what kind of tweet this was. \n It says: \""+content+"\" \n\nFor Assertion, press '1', \nfor Correction Of Own Mistake, press '2', \nfor Clarification, press '3', \nfor Debunking Other Outlets' Reports, press '4' \n Then hit return.\n\nif it's not clear, just hit Return/Enter, without pressing another key.\n\n")
	input = raw_input()
	if input == '1':
		Type="Assertion"
	if input == '2':
		Type="Correction"
	if input == '3':
		Type="Clarification"
	if input == '4':
		Type="Debunk"
	if input =='':
		Type="Unclear"
	print("\n\n\n Was it accurate?\n At Time: "+twittimeStamp+" it said: "+content+" \n\n For Accurate, press '1' Then hit return.\n For Inaccurate, press '0' Then hit return\n For Unsure, Just hit return \n\n ")
	input = raw_input()
	if input =="1":
		Accuracy='True'
	if input =="0":
		Accuracy='False'
	if input =="":
		Accuracy='Unsure'
	print("\n\n\nThanks, Did it mention sources? \n It says: \""+content+"\" \n\nFor Named Official Sources, press '1', \nfor Other Media, press '2', \nfor Own Sources, press '3', \nfor A straight out \"This is the Truth, with no attribution\", press '4' \nThen hit return.\n\nif it's not clear, just hit Return/Enter, without pressing another key.\n\n")
	input = raw_input()
	if input == '1':
		Attribution="Named Official Sources"
	if input == '2':
		Attribution="Other Media"
	if input == '3':
		Attribution="Own Sources"
	if input == '4':
		Attribution="No Attribution"
	if input =='':
		Attribution="Unclear"



	output = {'Type':Type,'Content':content,'Attribution':Attribution,'Author':str(jsonData['author_name']),'retweetsPerFollower':retweetsPerFollower,'favoritesPerFollower':favoritesPerFollower,'retweets':retweets,'favorites':favorites,'followers':followers,'TweetURL':TweetURL,'Time Stamp':twittimeStamp, 'Accuracy':Accuracy}

	return output

listofTweets=['https://twitter.com/Boston_Police/status/325409894830329856']
	



#This should probably come in from a storify or something, but for the moment, I'm passing it manually.
'''
listofTweets=['https://twitter.com/nypost/statuses/323896172299288577','https://twitter.com/nypost/statuses/323901175269314561','https://twitter.com/nypost/status/324571144948703232','https://twitter.com/nypost/statuses/324238174228451329','https://twitter.com/AP/status/324578507290185728','https://twitter.com/Reuters/status/324578856872849408','https://twitter.com/BuzzFeedNews/status/324579672191029248','https://twitter.com/nypost/status/324579553668390912','https://twitter.com/ReutersUS/status/324580832381661184','https://twitter.com/ABC/status/324581007053434880','https://twitter.com/AP/status/324583755350147072','https://twitter.com/CBSNews/status/324584027166228480','https://twitter.com/catesish/status/324583978889793537','https://twitter.com/FoxNews/status/324584418196983809','https://twitter.com/ellievhall/status/324584790156251137','https://twitter.com/paulafaris/status/324584392766930944','https://twitter.com/todayshow/status/324585223088136192','https://twitter.com/CNN/status/324586553441677315','https://twitter.com/Reuters/status/324589083559092224','https://twitter.com/CNN/status/324721784723210240','https://twitter.com/BostonGlobe/status/324589433875734528','https://twitter.com/Boston_Police/status/324591574807891968','https://twitter.com/CNN/status/324721784723210240','https://twitter.com/nypost/status/324593024896208896','https://twitter.com/CBSNews/status/324593633275834369','https://twitter.com/BloombergNews/status/324594004765319168','https://twitter.com/AP/status/324595020059537408','https://twitter.com/FoxNews/status/324595569731436546','https://twitter.com/FBIBoston/status/324598215536173056','https://twitter.com/FoxNews/status/324890629945577473','https://twitter.com/nypost/status/324851511651864576']
'''

ListOfAttention=[]
for tweet in listofTweets:
	print tweet
	ListOfAttention.append(TweetInput(tweet))

ListOfAttention



