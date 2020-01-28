import os
import discord
from discord.ext import commands
import logging
import random
import time
import asyncio


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = commands.Bot(command_prefix='$', help_command=None)
# client = discord.Client
TOKEN = 'NjY5MjYwOTU2NzY5MDU4ODY4.XitObg.CHG4AioEpx9sYHESfMsYaT_2bMM'

channels = {
		'general': 627271589062508566,
		'aux1': 602663309170311173,
		'aux2': 670503655308263434,
}

newUsrMsg = '''Welcome to the Easy Engineering server! Please say which course you are currently taking so a admin can update your role. If you have any questions regarding the server feel free to ask. Please read #rules. Remember we are all here to learn and help each so be respectful to your fellow students. \nDISCLAIMER: This bot is in no way affiliated with Dr. Carnal or TNTECH in anyway.'''

RANDOM_MESSAGES_DAY = 2
messageTimes = []
quotesSaid = 0

#basic function for checking if a messages author is the bot itself
def is_me(m):
	return m.author == client.user

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	client.loop.create_task(schedular())

# @client.event
# async def on_member_join(member):

# 	#stops the bot from messaging when itself joins
# 	if is_me(member):
# 		return

# 	print('Member called ' + member.name + ' joined')
# 	try:
# 		channel = client.get_channel(channels['aux1'])
# 		await channel.send(member.mention + ' ' + newUsrMsg)
# 		print('Sent welcome msg to ' + member.name)
# 	except:
# 		print('ERR: Could not send welcome msg.')

# @client.event
# async def on_message(message):
# 	print("Got message")
# 	if is_me(message):
# 		return

# 	if message.content.startswith('$'):
		
# 		if ('$echo' in message.content):
# 			newMsg = message.content.replace('$echo', '')
# 			await message.channel.send(newMsg)

def getTimeHours():
	hour = int(time.strftime('%H'))
	minute = int(time.strftime('%M'))
	minutes = hour + (minute / 60)
	return minutes

def genRandomTime():
	global quotesSaid
	global messageTimes
	quotesSaid = 0
	for i in range(RANDOM_MESSAGES_DAY):
		randTime = random.uniform(8, 20)
		messageTimes.append(randTime)
	messageTimes.sort()
	
async def random_quote():
	global quotesSaid
	global messageTimes
	if(getTimeHours() >= messageTimes[quotesSaid]):
		if quotesSaid <= RANDOM_MESSAGES_DAY:
			# quotes = getQuotes()
			try:
				print('Sending quote.')
				general = client.get_channel(channels['aux1'])
				# await general.send(quotes[random.randint(0, len(quotes)-1)])
				await general.send(f"Testing MessageTimes = {messageTimes}")
			except:
				print('EER: Failed sending quote.')
			quotesSaid += 1


def one_minute_loop():
	pass
async def five_minute_loop():
	await random_quote()
def thirty_minute_loop():
	pass
def one_hourly_loop():
	pass
def six_hour_loop():
	pass
def daily_loop():
	genRandomTime()

async def schedular():
	minute = 0
	while True:
		
		if (not(minute % 24 * 60) or not(minute)):
			daily_loop()
		if (not(minute % 6 * 60) or not(minute)):
			six_hour_loop()
		if (not(minute % 60) or not(minute)):
			one_hourly_loop()
		if (not(minute % 30) or not(minute)):
			thirty_minute_loop()
		if (not(minute % 5) or not(minute)):
			await five_minute_loop()

		one_minute_loop()

		await asyncio.sleep(60)

		minute += 1
		if (minute >= 24 * 60):
			minute = 0
		


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


client.run(TOKEN)

