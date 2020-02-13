import os
import discord
from discord.ext import commands
import logging
import asyncio
import random
from datetime import datetime, date, time, timedelta


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

cmdSym = '$'
channels = {
		'general': 602663309170311173,
		'C1-Q': 671814810278559774,
		'C2-Q': 670503709989404732,
}
newUsrMsg = '''Welcome to the Easy Engineering server! Please say which course you are currently taking so a admin can update your role. If you have any questions regarding the server feel free to ask. Please read <#670503655308263434>. Remember we are all here to learn and help each so be respectful to your fellow students. \nDISCLAIMER: This bot is in no way affiliated with Dr. Carnal or TNTECH in anyway.'''
now = datetime.today()
resetTime = now.replace(day=now.day+1, hour=8, minute=0)
general = None

general = None

RANDOM_MESSAGES_DAY = 2
messageTimes = []
quotesSaid = 0

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

client = commands.Bot(command_prefix='$', help_command=None)

def is_me(m):
	return m.author == client.user


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	global general  # NEED TO FIND ALTERNATIVE
	general = discord.utils.find(lambda c: c.name == 'general', client.get_all_channels())
	# client.loop.create_task(random_quote())
	client.loop.create_task(important_reminders())


@client.event
async def on_member_join(member):
	# stops the bot from messaging when itself joins
	if is_me(member):
		return

	print('Member called ' + member.name + ' joined')
	try:
		await asyncio.sleep(2)
		# general = client.get_channel(channels['aux1'])
		general = client.get_channel(channels['general'])
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
		await message.channel.send('Hello!')

	if message.content.startswith(cmdSym + 'final'):
		dates = getDates()
		if message.channel == client.get_channel(channels['C1-Q']):
			await message.channel.send(message.author.mention + 'The final is on ' + str(dates[3][0]) + ' at ' + str(dates[3][1]) + ' to ' + str(dates[3][2]))
		if message.channel == client.get_channel(channels['C2-Q']):
			await message.channel.send(message.author.mention + 'The final is on ' + str(dates[7][0]) + ' at ' + str(dates[7][1]) + ' to ' + str(dates[7][2]))

	if message.content.startswith(':thumbsup:'):
    
#for sum reason on_message prevents commands from running

# @client.event
# async def on_message(message):
# 	if is_me(message):
# 		return

# 	if message.content.startswith('/hello'):
# 		await message.channel.send('Hello!')

# 	if message.content.startswith(cmdSym + 'final'):
# 		dates = getDates()
# 		if message.channel == client.get_channel(channels['C1-Q']):
# 			await message.channel.send(message.author.mention + 'The final is on ' + str(dates[3][0]) + ' at ' + str(dates[3][1]) + ' to ' + str(dates[3][2]))
# 		if message.channel == client.get_channel(channels['C2-Q']):
# 			await message.channel.send(message.author.mention + 'The final is on ' + str(dates[7][0]) + ' at ' + str(dates[7][1]) + ' to ' + str(dates[7][2]))

	# if message.content.startswith(':thumbsup:'):

	# 	await message.channel.send('Send me that 👍 reaction, mate')

	# 	def check(reaction, user):
	# 		return user == message.author and str(reaction.emoji) == '👍'

	# 	try:
	# 		reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
	# 	except asyncio.TimeoutError:
	# 		await message.channel.send('👎')
	# 	else:
	# 		await message.channel.send('👍')


@client.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)

@client.command()
async def get(ctx, arg):
	if (arg == 'help'):
		await ctx.send('Arguments: email, website')
	elif (arg == 'email'):
		await ctx.send('CharlesLC@tntech.edu')
	elif (arg == 'website'):
		await ctx.send('https://clcee.net/clc_ece/')
	else:
		await ctx.send('I don\'t know what you are asking, read the syllabus')

@client.command()
async def about(ctx):
	await ctx.send('I am designed give some amusment, annoyance, and on rary occasions help to all jedi (EE/Compe) in training\nI am in no way affiliated with Dr. Charles Carnal')

@client.command()
async def help(ctx):
	await ctx.send('Avalible commands:\n' +
				   'About - gives general info about me, CarnBot\n' + 
				   'get - quick way to get public info on Dr. Charles Carnal and his courses\n' +
				   'echo - echo rest of message'
				   )
		try:
			reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await message.channel.send('👎')
		else:
			await message.channel.send('👍')


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
			await discord.utils.sleep_until(resetTime)
			quotesSaid = 0


async def send_reminders(channel, today, date, testNum):
	testNum = str(testNum)
	dateDelta = date - today.date()
	# print('checking to send reminder with dateDelta = ' + str(dateDelta))
	dateDelta = dateDelta.days
	if dateDelta == 14:
		print('sending 2 week reminder')
		await channel.send('REMINDER: TEST ' + testNum + ' is 2 weeks away!')
	elif dateDelta == 7:
		print('sending 1 week reminder')
		await channel.send('REMINDER: TEST ' + testNum + ' is a week away! If you are still having trouble with some concepts, remember to ask questions or utilize tutoring.')
	elif dateDelta == 3:
		print('sending 3 day reminder')
		await channel.send('REMINDER: TEST ' + testNum + ' is 3 days away! Utilize tutoring if you need it!!!')
	elif dateDelta == 1:
		print('sending 1 day reminder')
		await channel.send("RED ALERT: TEST " + testNum + " is TOMORROW!!! If you haven't started studying yet, don't bother starting! Rethink what you are doing and start thinking of alternative majors.")


async def important_reminders():
	iDates = getDates()
	Circuits1 = iDates[:4]
	Circuits2 = iDates[4:]
	while True:
		today = datetime.today()
		C1_Channel = client.get_channel(channels['C1-Q'])
		C2_Channel = client.get_channel(channels['C2-Q'])
		try:
			# Circuits 1
			if today.date() < Circuits1[0]:
				await send_reminders(C1_Channel, today, Circuits1[0], 1)
			elif today.date() < Circuits1[1]:
				await send_reminders(C1_Channel, today, Circuits1[1], 2)
			elif today.date() < Circuits1[2]:
				await send_reminders(C1_Channel, today, Circuits1[2], 3)
			elif today.date() < Circuits1[3][0]:
				dateDelta = Circuits1[3][0] - today.date()
				if dateDelta.days == 14:
					await C1_Channel.send('REMINDER: The FINAL is 2 weeks away!')
				elif dateDelta.days == 7:
					await C1_Channel.send('REMINDER: The FINAL is a week away! If you are still having trouble with some concepts, remember to ask questions or utilize tutoring.')
				elif dateDelta.days == 3:
					await C1_Channel.send('REMINDER: The FINAL is 3 days away! Utilize tutoring if you need it!!!')
				elif dateDelta.days == 1:
					await C1_Channel.send("RED ALERT: FINAL is TOMORROW at " + str(Circuits1[3][1]) + " to " + str(Circuits1[3][2]) + "!!! If you haven't started studying yet, don't bother starting! Start getting prepared to take this class again next semester.")
			# Circuits 2
			if today.date() < Circuits2[0]:
				await send_reminders(C2_Channel, today, Circuits2[0], 1)
			elif today.date() < Circuits2[1]:
				await send_reminders(C2_Channel, today, Circuits2[1], 2)
			elif today.date() < Circuits2[2]:
				await send_reminders(C2_Channel, today, Circuits2[2], 3)
			elif today.date() < Circuits2[3][0]:
				dateDelta = Circuits2[3][0] - today.date()
				if dateDelta.days == 14:
					await C2_Channel.send('REMINDER: The FINAL is 2 weeks away!')
				elif dateDelta.days == 7:
					await C2_Channel.send('REMINDER: The FINAL is a week away! If you are still having trouble with some concepts, remember to ask questions or utilize tutoring.')
				elif dateDelta.days == 3:
					await C2_Channel.send('REMINDER: The FINAL is 3 days away! Utilize tutoring if you need it!!!')
				elif dateDelta.days == 1:
					await C2_Channel.send("RED ALERT: FINAL is TOMORROW at " + str(Circuits2[3][1]) + " to " + str(Circuits2[3][2]) + "!!! If you haven't started studying yet, don't bother starting! Start getting prepared for taking this class again next semester.")
		except:
			print("ERR: Couldn't check and send test reminders.")
		await discord.utils.sleep_until(resetTime)

client.run('NjY5MjYwOTU2NzY5MDU4ODY4.XitObg.CHG4AioEpx9sYHESfMsYaT_2bMM')