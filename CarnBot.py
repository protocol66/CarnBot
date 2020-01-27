import os
import discord
import logging
import asyncio
import random
from datetime import datetime, date, time

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

channels = {
		'general': 627271589062508566,
		'aux1': 602663309170311173,
		'aux2': 670503655308263434,
}
newUsrMsg = '''Welcome to the Easy Engineering server! Please say which course you are currently taking so a admin can update your role. If you have any questions regarding the server feel free to ask. Please read <#670503655308263434>. Remember we are all here to learn and help each so be respectful to your fellow students. \nDISCLAIMER: This bot is in no way affiliated with Dr. Carnal or TNTECH in anyway.'''
general = None


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


client = discord.Client()


def is_me(m):
	return m.author == client.user


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	global general  # NEED TO FIND ALTERNATIVE
	general = discord.utils.find(lambda c: c.name == 'general', client.get_all_channels())
	client.loop.create_task(random_quote())


@client.event
async def on_member_join(member):
	# stops the bot from messaging when itself joins
	if is_me(member):
		return

	print('Member called ' + member.name + ' joined')
	try:
		await asyncio.sleep(2)
		# general = client.get_channel(channels['aux1'])
		await general.send(member.mention + ' ' + newUsrMsg)
		print('Sent welcome msg to ' + member.name)
	except:
		print('ERR: Could not send welcome msg.')


@client.event
async def on_message(message):
	print("Got message")
	if is_me(message):
		return

	if message.content.startswith('/hello'):
		await message.general.send('Hello!')

	if message.content.startswith(':thumbsup:'):

		await message.general.send('Send me that 👍 reaction, mate')

		def check(reaction, user):
			return user == message.author and str(reaction.emoji) == '👍'

		try:
			reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await general.send('👎')
		else:
			await general.send('👍')


async def random_quote():
	quotesSaid = 0
	while True:
		if quotesSaid < 2:
			quotes = getQuotes()
			try:
				print('Sending quote.')
				# general = client.get_channel(channels['aux1'])
				await general.send(quotes[random.randint(0, len(quotes)-1)])
			except:
				print('EER: Failed sending quote.')
			quotesSaid += 1
			await asyncio.sleep(random.randint(3*60*60, 12*60*60))
		else:
			now = datetime.today()
			resetTime = now.replace(day=now.day+1, hour=8, minute=0)
			await discord.utils.sleep_until(resetTime)
			quotesSaid = 0


def send_reminders(channel, today, date, testNum):
	dateDelta = date - today
	if dateDelta.days == 14:
		channel.send('REMINDER: TEST ' + testNum + ' is 2 weeks away!')
	elif dateDelta == 7:
		channel.send('REMINDER: TEST ' + testNum + ' is a week away! If you are still having trouble with some concepts, remember to ask questions or utilize tutoring.')
	elif dateDelta == 3:
		channel.send('REMINDER: TEST ' + testNum + ' is 3 days away! Utilize tutoring in you need it!!!')
	elif dateDelta == 1:
		channel.send("RED ALERT: TEST " + testNum + " is TOMORROW!!! If you haven't started studying yet, don't bother starting! Rethink what you are doing and start thinking of alternative majors.")


async def important_reminders():
	iDates = getDates()
	Circuits1 = iDates[:4]
	Circuits2 = iDates[4:]
	while True:
		today = datetime.today()
		today = today.replace(hour=8, minute=0, microsecond=0)
		C1_Channel = client.get_channel(channels['aux2'])
		C2_Channel = client.get_channel(channels['aux3'])
		# Circuits 1
		if today < Circuits1[0]:
			send_reminders(C1_Channel, today, Circuits1[0], 1)
		elif today < Circuits1[1]:
			send_reminders(C1_Channel, today, Circuits1[1], 2)
		elif today < Circuits1[2]:
			send_reminders(C1_Channel, today, Circuits1[2], 3)
		elif today < Circuits1[3][0]:
			dateDelta = Circuits1[3][0] - today
			if dateDelta.days == 14:
				C1_Channel.send('REMINDER: The FINAL is 2 weeks away!')
			elif dateDelta == 7:
				C1_Channel.send('REMINDER: The FINAL is a week away! If you are still having trouble with some concepts, remember to ask questions or utilize tutoring.')
			elif dateDelta == 3:
				C1_Channel.send('REMINDER: The FINAL is 3 days away! Utilize tutoring in you need it!!!')
			elif dateDelta == 1:
				C1_Channel.send("RED ALERT: FINAL is TOMORROW at " + str(Circuits1[3][1]) + " to " + str(Circuits1[3][2]) + "!!! If you haven't started studying yet, don't bother starting! Start getting prepared for taking this class again next semester.")
		# Circuits 2
		if today < Circuits2[0]:
			send_reminders(C2_Channel, today, Circuits2[0], 1)
		elif today < Circuits2[1]:
			send_reminders(C1_Channel, today, Circuits2[1], 2)
		elif today < Circuits1[2]:
			send_reminders(C1_Channel, today, Circuits2[2], 3)
		elif today < Circuits1[3][0]:
			dateDelta = Circuits1[3][0] - today
			if dateDelta.days == 14:
				C1_Channel.send('REMINDER: The FINAL is 2 weeks away!')
			elif dateDelta == 7:
				C1_Channel.send(
					'REMINDER: The FINAL is a week away! If you are still having trouble with some concepts, remember to ask questions or utilize tutoring.')
			elif dateDelta == 3:
				C1_Channel.send('REMINDER: The FINAL is 3 days away! Utilize tutoring in you need it!!!')
			elif dateDelta == 1:
				C1_Channel.send("RED ALERT: FINAL is TOMORROW at " + str(Circuits1[3][1]) + " to " + str(
					Circuits1[3][
						2]) + "!!! If you haven't started studying yet, don't bother starting! Start getting prepared for taking this class again next semester.")
		await asyncio.sleep(24*60*60)

# client.run('NjY5MjYwOTU2NzY5MDU4ODY4.XitObg.CHG4AioEpx9sYHESfMsYaT_2bMM')