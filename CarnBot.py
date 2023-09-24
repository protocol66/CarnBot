import os
import sys
import discord
from discord.ext import commands
import asyncio

# add path to sys.path
sys.path.append(os.path.realpath('.'))


import constants

#enables on member join function
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='$', help_command=None, intents=intents)
constants.client = client

from constants import *
from features import is_me, create_logger
from features import random_quote, important_reminders, dumbAssOfTheDay
from features import commands

logger = create_logger()
   

# start event loops
@client.event
async def on_ready():
	logger.info('Logged in as {0.user}'.format(client))
	# client.loop.create_task(random_quote())
	# client.loop.create_task(important_reminders())
	# client.loop.create_task(dumbAssOfTheDay())


@client.event
async def on_member_join(member: discord.Member):
	# stops the bot from messaging when itself joins
	if member == client.user:
		return

	logger.info('Member called ' + member.name + ' joined')
	try:
		await asyncio.sleep(2)
		general = client.get_channel(channels['general'])
		await general.send(member.mention + ' ' + NEWUSRMSG)
		logger.debug('Sent welcome msg to ' + member.name)
	except:
		logger.error('Could not send welcome msg.')


@client.event
async def on_message(message: discord.Message):
	logger.debug(f"Message from {message.author}: {message.content}")
	if is_me(message):
		return

	if (client.user.mentioned_in(message) and message.mention_everyone == False):
		logger.debug('Bot mentioned')
		await message.channel.send('Who fired that shot?')

	await client.process_commands(message)



if __name__ == '__main__':

	logger.info('Starting CarnBot...')
	try:
		with open('token.txt', 'r') as f:
			token = f.read()
		logger.debug('Loaded token file')
	except:
		logger.critical('Could not load token file')
		sys.exit(1)

	api_logger = create_logger('discord')
 
	client.run(token, log_formatter=root_logger_formatter, log_handler=root_logger_handlers[0], root_logger=True)
	