#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from twikit import Client
import feedparser
import asyncio
from bs4 import BeautifulSoup

USERNAME = 'USERNAME'
EMAIL = 'EMAIL@EXAMPLE.COM'
PASSWORD = 'PASSWORD'

feedsUrl = ['https://example.com/rss1.xml', 'https://example.com/rss2.xml']
hashtags = '#feedTwitter #Twitter'

filename = 'feedTwitter-db.txt'
maxmsg = [1, 1]
maxchar = [500, 500]
posts = []
links = ''

for idx, feedUrl in enumerate(feedsUrl):
	nbmsg = 0
	feed = feedparser.parse(feedUrl)

	for item in reversed(feed.entries):
		send = True
		soup = BeautifulSoup(item.title, 'lxml')
		title = soup.text
		link = item.link
		tweet = title + '\n\n' + link

		if hashtags:
			tweet += '\n\n' + hashtags

		if len(tweet) > maxchar[idx]:
			send = False

		if os.path.exists(filename):
			db = open(filename, "r+")
			entries = db.readlines()
		else:
			db = open(filename, "a+")
			entries = []

		for entry in entries:
			if link in entry:
				send = False

		if send:
			posts.append(tweet)
			links += link + '\n'

			nbmsg = nbmsg + 1
			if nbmsg >= maxmsg[idx]:
				break

		db.close()

if posts:
	clientTwitter = Client('fr-FR')

	async def twitter():
		if os.path.exists('cookies.json'):
			clientTwitter.load_cookies('cookies.json')
		else:
			await clientTwitter.login(
				auth_info_1=USERNAME,
				auth_info_2=EMAIL,
				password=PASSWORD
			)
			clientTwitter.save_cookies('cookies.json')

		for idy, l in enumerate(posts):
			await clientTwitter.create_tweet(l)

		if os.path.exists(filename):
			db = open(filename, "r+")
			entries = db.readlines()
		else:
			db = open(filename, "a+")
			entries = []

		db.write(links)
		db.flush()
		db.close()

	asyncio.run(twitter())
