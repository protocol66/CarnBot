import os
import discord
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

channels = {
		'general': 627271589062508566,
		'aux1': 602663309170311173,
		'aux2': 670503655308263434,
}

newUsrMsg = '''Welcome to the Easy Engineering server! Please say which course you are currently taking so a admin can update your role. If you have any questions regarding the server feel free to ask. Please read #rules. Remember we are all here to learn and help each so be respectful to your fellow students. \nDISCLAIMER: This bot is in no way affiliated with Dr. Carnal or TNTECH in anyway.'''

def is_me(m):
    return m.author == client.user

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
	#stops the bot from messaging when itself joins
	if is_me(member):
		return

	print('Member called ' + member.name + ' joined')
	try:
		channel = client.get_channel(channels['aux1'])
		await channel.send(member.mention + ' ' + newUsrMsg)
		print('Sent welcome msg to ' + member.name)
	except:
		print('ERR: Could not send welcome msg.')

@client.event
async def on_message(message):
	print("Got message")
	if is_me(message):
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')

	if message.content.startswith(':thumbsup:'):

		await message.channel.send('Send me that 👍 reaction, mate')

		def check(reaction, user):
			return user == message.author and str(reaction.emoji) == '👍'

		try:
			reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await channel.send('👎')
		else:
			await channel.send('👍')

client.run('NjY5MjYwOTU2NzY5MDU4ODY4.XitObg.CHG4AioEpx9sYHESfMsYaT_2bMM')
