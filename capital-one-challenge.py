# Created by Jeffrey Van
#Last modified: 10/29/15
#Citations: http://www.beartech.ca/writeups/?tag=Instagram-Python

from random import randint
import sys
from collections import OrderedDict
from instagram.client import InstagramAPI
import string
import unicodedata

client_id = 'YOUR CLIENT ID GOES HERE'
client_secret = 'YOUR CLIENT SECRET GOES HERE'
access_token = 'YOUR ACCESS TOKEN GOES HERE'
client_ip = 'YOUR CLIENT\'S IP ADDRESS GOES HERE'
api = InstagramAPI(client_id=client_id, client_secret=client_secret,client_ips= client_ip,access_token= access_token)

media_all_ids=[]
likes = []
users = []
captions = []
tags = []
positive = 0
negative = 0
neutral = 0
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

#get recent media ids with the tag "CapitalOne", only get the most recent 80
#tag_recent_media returns 2 variables, the media ID in an array and the next
#url for the next page
media_ids,next = api.tag_recent_media(tag_name='CapitalOne', count=20)


#obtain the max_tag_id to use to get the next page of results
temp,max_tag=next.split('max_tag_id=')
max_tag=str(max_tag)

for media_id in media_ids:
    users.append(media_id.user.id)
    media_all_ids.append(media_id.id)
    captions.append(media_id.caption.text)
    tags.append(media_id.tags)
    post_likes = api.media_likes(media_id.id)
    likes.append(len(post_likes))


for user_id in users:
    users_info = api.user(user_id=user_id)
    print users_info.username + ' currently has ' + str(users_info.counts['media']) + ' posts.'
    print users_info.username + ' currently has ' + str(users_info.counts['followed_by']) + ' followers.'
    print users_info.username + ' is currently following ' + str(users_info.counts['follows']) + ' people.'


# list of positive key-words and emojis, including smiley faces, hearts, celebrations, money bags, etc.
positive_word_list = ['thanks', 'great', 'appreciate', 'awesome', 'good', u'\U0001F60D', u'\U0001F60A', u'\U0001F44D',
    u'\U0001F44C', u'\U0001F498', u'\u2764', u'\U0001F493', u"\U0001F614", u"\U0001F495", u"\U0001F496", u"\U0001F497",
    u"\U0001F499", u"\U0001F49A", u"\U0001F49B", u"\U0001F49C", u"\U0001F49D", u"\U0001F49E", u"\U0001F389", u"\U0001F38A",
    u"\U0001F4B0", u"\U0001F4B8", u"\U0001F4B3", u"\U0001F603", u"\U0001F64C"]

#list of negative key-words and emojis, including frowning faces, broken hearts, etc.
negative_word_list = ['hate', 'ugh', 'dumb', 'unsatisfactory', 'terrible', 'bad', u"\U0001F623", u"\U0001F625",
    u"\U0001F62B", u"\U0001F612", u"\U0001F614", u"\U0001F615", u"\U0001F624", u"\U0001F622", u"\U0001F62D", u"\U0001F629",
    u"\U0001F621", u"\U0001F620", u"\U0001F44E", u"\U0001F4A9"]

for cap in captions:
    cap = [unicode(cap).translate(remove_punctuation_map)]
    cap = ' '.join(cap)
    cap = cap.lower()
    cap = cap.split()
    pos = [i for i in positive_word_list if i in cap]
    neg = [i for i in negative_word_list if i in cap]
    if pos != []:
        positive = positive + 1
    elif neg != []:
        negative = negative + 1
    elif neg == [] and pos == []:
        neutral = neutral + 1
    pos[:] = []
    neg[:] = []


counter = 1

#the while loop will go through the first 3 pages of results, you can increase this
# but you also need to increase the count above.
while next and counter < 3 :
	more_media, next = api.tag_recent_media(tag_name='CapitalOne', max_tag_id=max_tag)
	temp,max_tag=next.split('max_tag_id=')
	max_tag=str(max_tag)
	for media_id2 in more_media:
		media_all_ids.append(media_id2.id)
	# print len(media_all_ids)
	counter+=1

#remove dublictes if any.
media_all_ids=list(OrderedDict.fromkeys(media_all_ids))


print 'a list of the amount of likes on each post of the 20 most recent posts, in no particular order: ' + str(likes)
print 'number of positive posts: ' + str(positive)
print 'number of negative posts: ' + str(negative)
print 'number of neutral posts: ' + str(neutral)
