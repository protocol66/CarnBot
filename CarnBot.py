import os
import sys
import discord
from discord.ext import commands
import asyncio

# add path to sys.path
sys.path.append(os.path.realpath('.'))

#enables on member join function
intents = discord.Intents.default()
intents.members = True

import constants
constants.client = commands.Bot(command_prefix='$', help_command=None, intents=intents)
from constants import *

from features import is_me
from features import random_quote, important_reminders, dumbAssOfTheDay

from features import commands


# start event loops
@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	# client.loop.create_task(random_quote())
	# client.loop.create_task(important_reminders())
	client.loop.create_task(dumbAssOfTheDay())


@client.event
async def on_member_join(member: discord.Member):
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
async def on_message(message: discord.Message):
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





if __name__ == '__main__':
	with open('token.txt', 'r') as f:
		token = f.read()

	client.run(token)