import discord
import asyncio
import random
import sys
import os


from constants import client, persistent_roles, channels, NEWUSRMSG
from .utils import create_logger, getDates, getPanicGIFS

logger = create_logger('commands')

@client.slash_command(name='echo', description='Echoes the message')
async def echo(ctx:discord.context.ApplicationContext, 
			message:discord.Option(discord.SlashCommandOptionType.string, description='Message to Echo'), 
			channel:discord.Option(discord.SlashCommandOptionType.channel, description='Channel to send to, defauts channel message is sent in')=''):
	
	logger.debug('echo called')
	logger.debug(f'message = {message}, channel = {channel}')

	if(channel != ''):
		try:
			await channel.send(message)
			await ctx.respond(f'Message sent to {channel}')
		except:
			await ctx.respond('Invalid channel', ephemeral=True, delete_after=10)
	else:
		await ctx.respond(" ".join(message))

@client.slash_command(name='get', description='Gets the requested infomation.')
async def get(ctx:discord.context.ApplicationContext, 
			message:discord.Option(discord.SlashCommandOptionType.string, description='Information to request, either "website" or "email"')):
	if message == '':
		await ctx.respond('Arguments: *help*, *email*, *website*')
	elif message == 'help':
		await ctx.respond('Arguments: *help*, *email*, *website*')
	elif message == 'email':
		await ctx.respond('__*CharlesLC@tntech.edu*__')
	elif message == 'website':
		await ctx.respond('https://clcee.net/clc_ece/')
	else:
		await ctx.respond('I don\'t know what you are asking, read the syllabus')

@client.slash_command(name='about', description='Describes what the purpose of the bot is')
async def about(ctx:discord.context.ApplicationContext):
 	await ctx.respond('I am designed to give some amusement, annoyance, and on rare occasions help to all jedi (EE/CompE) in training\n*I am in no way affiliated with Dr. Charles Carnal*')

# # @client.command()
# # async def help(ctx):
# # 	await ctx.send('```Available commands:\n' +
# # 					'about - gives general info about me, DarthCarnal\n' +
# # 					'get - quick way to get public info on Dr. Charles Carnal and his courses\n' +
# # 					'echo - echo rest of message\n' +
# # 					'final - get time and date of final\n' +
# # 					'panic - makes bot panic```')


# @client.command()
# async def final(ctx):
# 	dates = getDates()
# 	if ctx.channel == client.get_channel(channels['C1-Q']):
# 		await ctx.channel.send(
# 			ctx.author.mention + ' The final is on **' + str(dates[3][0]) + '** at *' + str(dates[3][1]) + '* to *' + str(
# 				dates[3][2]) + '*')
# 	if ctx.channel == client.get_channel(channels['C2-Q']):
# 		await ctx.channel.send(
# 			ctx.author.mention + ' The final is on **' + str(dates[7][0]) + '** at *' + str(dates[7][1]) + '* to *' + str(
# 				dates[7][2]) + '*')
# 	if ctx.channel == client.get_channel(channels['general']):
# 		await ctx.channel.send(
# 			ctx.author.mention + '\n The **Circuits 1** final is on **' + str(dates[3][0]) + '** at *' + str(dates[3][1]) + '* to *' + str(
# 				dates[3][2]) + '* \n The **Circuits 2** final is on **' + str(dates[7][0]) + '** at *' + str(dates[7][1]) + '* to *' + str(
# 				dates[7][2]) + '*')


# @client.command()
# async def reboot(ctx, arg):
# 	await ctx.send(f"Rebooting in {arg} minutes")
# 	await asyncio.sleep(int(arg)*60)
# 	os.execv(sys.executable, ['python'] + sys.argv)

# @client.command()
# async def shutdown(ctx):
# 	await ctx.send(f"Shuting Down")
# 	sys.exit()

# @client.command()
# async def pull(ctx):
# 	await ctx.send("Pulling From Github")
# 	await ctx.send(os.popen("git pull").read())
# 	#its working

# @client.command()
# async def panic(ctx):
# 	panicGifs = getPanicGIFS()
# 	gif = panicGifs['GIFS'][random.randint(1, panicGifs['numGifs'])]
# 	await ctx.channel.send(gif)


# @client.command()
# async def testNewMemberMsg(ctx):
# 	await ctx.channel.send(NEWUSRMSG)

# @client.command()
# async def nukeChats(ctx):
# 	for channel in ctx.guild.channels:
# 		if ((channel.name == "discussion") or (channel.name == "lab") or (channel.name == "past-work")):
# 			await channel.clone()
# 			await channel.delete()

# @client.command()
# async def pull(ctx):
# 	await ctx.send("Pulling From Github")
# 	await ctx.send(os.popen("git pull").read())
# 	#its working

# @client.command()
# async def panic(ctx):
# 	panicGifs = getPanicGIFS()
# 	gif = panicGifs['GIFS'][random.randint(1, panicGifs['numGifs'])]
# 	await ctx.channel.send(gif)


# @client.command()
# async def testNewMemberMsg(ctx):
# 	await ctx.channel.send(NEWUSRMSG)

# @client.command()
# async def nukeChats(ctx):
# 	for channel in ctx.guild.channels:
# 		if ((channel.name == "discussion") or (channel.name == "lab") or (channel.name == "past-work")):
# 			await channel.delete()
# 	for cat in ctx.guild.categories:
# 		if "ECE" in cat.name:
# 			await cat.delete()

# @client.command()
# async def createChats(ctx):
# 	for role in ctx.guild.roles:
# 		overwrites = {
# 			ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
# 			role: discord.PermissionOverwrite(read_messages=True)
# 		}

# 		if ("ECE" in role.name):
# 			category = await ctx.guild.create_category(role.name, overwrites=overwrites)
# 			await ctx.guild.create_text_channel("discussion", category=category, overwrites=overwrites)
# 			await ctx.guild.create_text_channel("past-work", category=category, overwrites=overwrites)
# 			if("/" in role.name):
# 				await ctx.guild.create_text_channel("lab", category=category, overwrites=overwrites)

# @client.command()
# async def clearRoles(ctx):
# 	rolesWithPersistence = []
# 	rolesWithPersistence.append(discord.utils.get(ctx.guild.roles, name="Alumni"))
# 	rolesWithPersistence.append(discord.utils.get(ctx.guild.roles, name="Professor"))
# 	rolesWithPersistence.append(discord.utils.get(ctx.guild.roles, name="Graduate Student"))
# 	for member in ctx.guild.members:
# 		if (any(r in member.roles for r in rolesWithPersistence)):
# 			continue
# 		for role in member.roles:
# 			if (not (role.name in persistent_roles)):
# 				try:
# 					await member.remove_roles(role)
# 				except:
# 					print("Failed to remove role " + role.name + " from " + member.name)
