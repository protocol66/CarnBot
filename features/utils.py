from datetime import datetime, date, time

from constants import client

def getPanicGIFS():
	with open('panic_gifs.txt', 'r') as f:
		text = f.read()
		lines = text.split('\n')
		numGif = 0
		GIFS = {}
		for i in lines:
			if i != '':
				numGif += 1
				GIFS[numGif] = i
		return {'GIFS': GIFS, 'numGifs': numGif}

def is_me(m):
	return m.author == client.user

def getQuotes():
	with open('quotes.txt', 'r') as f:
		text = f.read()
		quotes = text.split('\n')
	return quotes

def getDates():
	with open('important-dates.txt', 'r') as f:
		text = f.read()
		lines = text.split('\n')
		dates = []
		year = datetime.today().year
		for n in lines:
			n = n.split(' ')
			if len(n) == 2:
				d = date(year, int(n[0]), int(n[1]))
				dates.append(d)
			elif len(n) == 6:
				final = []
				d = date(year, int(n[0]), int(n[1]))
				final.append(d)
				t1 = time(int(n[2]), int(n[3]))
				t2 = time(int(n[4]), int(n[5]))
				final.append(t1)
				final.append(t2)
				dates.append(final)
		return dates