import os
import sys
import discord
from discord.ext import commands
import logging
import asyncio
import pickle
import random
from datetime import datetime, date, time, timedelta


###############
###  setup  ###
###############

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#enables on member join function
intents = discord.Intents.default()
intents.members = True

# client = discord.Client()
client = commands.Bot(command_prefix='$', help_command=None, intents=intents)

channels = {
		'general': 627271589062508566,
		'C1-Q': 654556140415221776,
		'C2-Q': 654555766660792340,
}

############################
###  constants and vars  ###
############################

# Globals Constants
NEWUSRMSG = '''Welcome to the Easy Engineering server! If you have any questions regarding the server feel free to ask. Please read <#627273181778018344>. Remember we are all here to learn and help each so be respectful to your fellow students. \nDISCLAIMER: This bot is in no way affiliated with Dr. Carnal or TNTECH in anyway.'''
RANDOM_MESSAGES_DAY = 2

# Global Variables, Doc Brown look away
# now = datetime.today()
# RmdResetTime = now.replace(day=now.day + 1, hour=8, minute=0)
# QtResetTime =
messageTimes = []


###########################
###  utility functions  ###
###########################

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


async def send_reminders(channel, today, date, testNum, gif):
	testNum = str(testNum)
	dateDelta = date - today.date()
	# print('checking to send reminder with dateDelta = ' + str(dateDelta))
	dateDelta = dateDelta.days
	if dateDelta == 14:
		print('sending 2 week reminder')
		await channel.send('__**REMINDER**__: **TEST ' + testNum + ' is 2 weeks away!**')
	elif dateDelta == 7:
		print('sending 1 week reminder')
		await channel.send('__**REMINDER**__: **TEST ' + testNum + ' is a week away!** If you are still having trouble with some concepts, remember to ask questions or utilize tutoring.')
	elif dateDelta == 3:
		print('sending 3 day reminder')
		await channel.send('__**REMINDER**__: **TEST ' + testNum + ' is 3 days away!** Utilize tutoring if you need it!!!')
	elif dateDelta == 1:
		print('sending 1 day reminder')
		await channel.send("__**RED ALERT**__: **TEST " + testNum + " is TOMORROW!!!** If you haven't started studying yet, don't bother starting! Rethink what you are doing and start thinking of alternative majors.\n" + gif)


#########################
###  event functions  ###
#########################

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	client.loop.create_task(random_quote())
	client.loop.create_task(important_reminders())


@client.event
async def on_member_join(member):
	# stops the bot from messaging when itself joins
	if member == client.user:
		return

	print('Member called ' + member.name + ' joined')
	try:
		await asyncio.sleep(2)
		general = client.get_channel(channels['general'])
		await general.send(member.mention + ' ' + NEWUSRMSG)
		print('Sent welcome msg to ' + member.name)
	except:
		print('ERR: Could not send welcome msg.')


@client.event
async def on_message(message):
	# print("Got message")
	if is_me(message):
		return
	# needed for commands to work

	if (client.user.mentioned_in(message) and message.mention_everyone == False):
		await message.channel.send('Who fired that shot?')

	# for testing
	if message.content.startswith('/hello'):
		await message.channel.send('Hello!')

	await client.process_commands(message)


###########################
###  command functions  ###
###########################

@client.command()
async def echo(ctx, *arg):

	if (not len(arg) or arg[0] == "help"):
		await ctx.send('Usage: del/delete <message>\n del/delete - deletes the original message')
		return

	delete = False

	if (arg[0] == "del" or arg[0] == "delete"):
		arg = arg[1:]
		delete = True
	
	if(ctx.message.channel_mentions):
		send_channel = ctx.message.channel_mentions[0]
		arg = arg[1:]
		await send_channel.send(" ".join(arg))
	else:
		await ctx.send(" ".join(arg))

	if (delete):
		await ctx.message.delete()


@client.command()
async def get(ctx, arg=''):
	if arg == '':
		await ctx.send('Arguments: *help*, *email*, *website*')
	elif arg == 'help':
		await ctx.send('Arguments: *help*, *email*, *website*')
	elif arg == 'email':
		await ctx.send('__*CharlesLC@tntech.edu*__')
	elif arg == 'website':
		await ctx.send('https://clcee.net/clc_ece/')
	else:
		await ctx.send('I don\'t know what you are asking, read the syllabus')


@client.command()
async def about(ctx):
	await ctx.send('I am designed give some amusement, annoyance, and on rare occasions help to all jedi (EE/CompE) in training\n*I am in no way affiliated with Dr. Charles Carnal*')


@client.command()
async def help(ctx):
	await ctx.send('```Available commands:\n' +
					'about - gives general info about me, DarthCarnal\n' +
					'get - quick way to get public info on Dr. Charles Carnal and his courses\n' +
					'echo - echo rest of message\n' +
					'final - get time and date of final\n' +
					'panic - makes bot panic```')


@client.command()
async def final(ctx):
	dates = getDates()
	if ctx.channel == client.get_channel(channels['C1-Q']):
		await ctx.channel.send(
			ctx.author.mention + ' The final is on **' + str(dates[3][0]) + '** at *' + str(dates[3][1]) + '* to *' + str(
				dates[3][2]) + '*')
	if ctx.channel == client.get_channel(channels['C2-Q']):
		await ctx.channel.send(
			ctx.author.mention + ' The final is on **' + str(dates[7][0]) + '** at *' + str(dates[7][1]) + '* to *' + str(
				dates[7][2]) + '*')
	if ctx.channel == client.get_channel(channels['general']):
		await ctx.channel.send(
			ctx.author.mention + '\n The **Circuits 1** final is on **' + str(dates[3][0]) + '** at *' + str(dates[3][1]) + '* to *' + str(
				dates[3][2]) + '* \n The **Circuits 2** final is on **' + str(dates[7][0]) + '** at *' + str(dates[7][1]) + '* to *' + str(
				dates[7][2]) + '*')


@client.command()
async def reboot(ctx, arg):
	await ctx.send(f"Rebooting in {arg} minutes")
	await asyncio.sleep(int(arg)*60)
	os.execv(sys.executable, ['python'] + sys.argv)

@client.command()
async def shutdown(ctx):
	await ctx.send(f"Shuting Down")
	sys.exit()

@client.command()
async def pull(ctx):
	await ctx.send("Pulling From Github")
	await ctx.send(os.popen("./pull.sh").read())
	#its working

@client.command()
async def panic(ctx):
	panicGifs = getPanicGIFS()
	gif = panicGifs['GIFS'][random.randint(1, panicGifs['numGifs'])]
	await ctx.channel.send(gif)


@client.command()
async def testNewMemberMsg(ctx):
	await ctx.channel.send(NEWUSRMSG)


########################
###  main functions  ###
########################

# well I have code this about 4 times, feel free to make fun
async def random_quote():
	while True:
		quoteTimes = []
		minInterval = timedelta(hours=3)
		now = datetime.today()
		nowDec = now.hour + now.minute/60
		print(f"Now is {nowDec}")

		try:
			file = open('randquote.lock', 'rb')
			lockTime = pickle.load(file)
			file.close()
		except IOError:
			lockTime = now.today() - timedelta(days=1)
		print(lockTime)
		if ((nowDec >= 8) and (nowDec < 20) and (now >= lockTime + timedelta(days=1))):
			for i in range(RANDOM_MESSAGES_DAY):
				quoteTimes.append(now.replace(hour=int(random.uniform(now.hour,19)), minute=int(random.uniform(now.minute,60))))

			quoteTimes.sort()
			print(f"quoteTimes is {quoteTimes}")
			for i in range(RANDOM_MESSAGES_DAY):
				if i != 0:
					if (quoteTimes[i] - quoteTimes[i-1]) < minInterval:
						print("ERR: quoteTime " + str(i) + " less than minInterval... recalculating")
						quoteTimes[i] = quoteTimes[i-1] + minInterval
			print(f"quoteTimes is {quoteTimes}")
			
			file = open('randquote.lock', 'wb')
			pickle.dump(now, file)
			file.close()

			for i in range(len(quoteTimes)):
				now = datetime.today()
				sleepTime = (quoteTimes[i] - now).total_seconds()
				print(f"sleepTime is {sleepTime}")
				await asyncio.sleep(sleepTime)

				quotes = getQuotes()
				try:
					print('Sending quote.')
					general = client.get_channel(channels['general'])
					await general.send(quotes[random.randint(0, len(quotes)-1)])
				except:
					print('EER: Failed sending quote.')

			now = datetime.today()
			# hour = 14 because the bot uses UTC time
			resetTime = now.replace(hour=14, minute=0) + timedelta(days=1)
			await discord.utils.sleep_until(resetTime)

		elif (nowDec < 8):
			now = datetime.today()
			# hour = 14 because the bot uses UTC time
			resetTime = now.replace(hour=14, minute=0)
			await discord.utils.sleep_until(resetTime)

		else:
			now = datetime.today()
			# hour = 14 because the bot uses UTC time
			resetTime = now.replace(hour=14, minute=0) + timedelta(days=1)
			await discord.utils.sleep_until(resetTime)


async def dumbAssOfTheDay():
	while True:
		randMem = random.choice(list(client.get_all_members()))
		role = discord.utils.get(randMem.guild.roles, name="Dumb Ass of the Day")
		for mem in role.members:
			await mem.remove_roles(role)
		await randMem.add_roles(role)

		now = datetime.today()
		resetTime =  now.replace(hour=8, minute=0) + timedelta(days=1)
		await discord.utils.sleep_until(resetTime)
		# sleep(10)
		await randMem.remove_roles(role)

async def important_reminders():
	
	while True:

		today = datetime.today()
		try:
			lockTime = pickle.load(open('reminders.lock', 'rb'))
		except IOError:
			lockTime = today.today() - timedelta(days=1)

		if (today.day >= lockTime.day + 1):
			
			iDates = getDates()
			Circuits1 = iDates[:4]
			Circuits2 = iDates[4:]

			C1_Channel = client.get_channel(channels['C1-Q'])
			C2_Channel = client.get_channel(channels['C2-Q'])
			panicGifs = getPanicGIFS()
			gif = panicGifs['GIFS'][random.randint(1, panicGifs['numGifs'])]
			try:
				# Circuits 1
				if today.date() < Circuits1[0]:
					await send_reminders(C1_Channel, today, Circuits1[0], 1, gif)
				elif today.date() < Circuits1[1]:
					await send_reminders(C1_Channel, today, Circuits1[1], 2, gif)
				elif today.date() < Circuits1[2]:
					await send_reminders(C1_Channel, today, Circuits1[2], 3, gif)
				elif today.date() < Circuits1[3][0]:
					dateDelta = Circuits1[3][0] - today.date()
					if dateDelta.days == 14:
						await C1_Channel.send('__**REMINDER**__: The **FINAL is 2 weeks away!**')
					elif dateDelta.days == 7:
						await C1_Channel.send('__**REMINDER**__: The **FINAL is a week away!** If you are still having trouble with some concepts, remember to ask questions or utilize tutoring.')
					elif dateDelta.days == 3:
						await C1_Channel.send('__**REMINDER**__: The **FINAL is 3 days away!** Utilize tutoring if you need it!!!')
					elif dateDelta.days == 1:
						await C1_Channel.send("__**RED ALERT**__: **FINAL is TOMORROW** at *" + str(Circuits1[3][1]) + "* to *" + str(Circuits1[3][2]) + "*!!! If you haven't started studying yet, don't bother starting! Start getting prepared to take this class again next semester.\n" + gif)
				# Circuits 2
				if today.date() < Circuits2[0]:
					await send_reminders(C2_Channel, today, Circuits2[0], 1, gif)
				elif today.date() < Circuits2[1]:
					await send_reminders(C2_Channel, today, Circuits2[1], 2, gif)
				elif today.date() < Circuits2[2]:
					await send_reminders(C2_Channel, today, Circuits2[2], 3, gif)
				elif today.date() < Circuits2[3][0]:
					dateDelta = Circuits2[3][0] - today.date()
					if dateDelta.days == 14:
						await C2_Channel.send('__**REMINDER**__: The **FINAL is 2 weeks away!**')
					elif dateDelta.days == 7:
						await C2_Channel.send('__**REMINDER**__: The **FINAL is a week away!** If you are still having trouble with some concepts, remember to ask questions or utilize tutoring.')
					elif dateDelta.days == 3:
						await C2_Channel.send('__**REMINDER**__: The **FINAL is 3 days away!** Utilize tutoring if you need it!!!')
					elif dateDelta.days == 1:
						await C2_Channel.send("__**RED ALERT**__: **FINAL is TOMORROW** at *" + str(Circuits2[3][1]) + "* to *" + str(Circuits2[3][2]) + "*!!! If you haven't started studying yet, don't bother starting! Start getting prepared for taking this class again next semester.\n" + gif)
			except:
				print("ERR: Couldn't check and send test reminders.")

			now = datetime.today()
			pickle.dump(now, open('reminders.lock', 'wb'))

			# 14 instead of 8 because the time is in utc
			resetTime = now.replace(hour=14, minute=0) + timedelta(days=1)
			await discord.utils.sleep_until(resetTime)
		else:
			now = datetime.today()
			resetTime = now.replace(hour=14, minute=0) + timedelta(days=1)
			await discord.utils.sleep_until(resetTime)

client.run('NjY5MjYwOTU2NzY5MDU4ODY4.XidP1g.C_RHn06IVeC7NKbwfh3KntzcEGs')
