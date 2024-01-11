import discord
import asyncio
import random
import sys
import os
import threading
import time
import logging


from constants import client, persistent_roles, channels, NEWUSRMSG
from features.misc import Confirmation
from .utils import create_logger, get_user_info, getDates, getPanicGIFS, is_admin, invalid_perm_response

logger = create_logger('commands')


@client.slash_command(name='echo', description='Echoes the message')
async def echo(ctx:discord.context.ApplicationContext, 
			message:discord.Option(discord.SlashCommandOptionType.string, description='Message to Echo'), 
			channel:discord.Option(discord.SlashCommandOptionType.channel, description='Channel to send to, defauts channel message is sent in')=''):
	
	message = str(message)
	logger.debug('echo called')
	logger.debug(f'message = {message}, channel = {channel}')

	if(channel != ''):
		try:
			await channel.send(message)
			await ctx.respond(f'Message sent to {channel}')
		except:
			await ctx.respond('Invalid channel', ephemeral=True, delete_after=10)
	else:
		await ctx.respond(message)


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


@client.slash_command(name='reboot', description='Reboots the bot after a specified amount of time')
async def reboot(ctx:discord.context.ApplicationContext, 
				 delay:discord.Option(discord.SlashCommandOptionType.integer, default=0, description='Time in minutes to reboot after')):
	
	logger.debug('reboot called')
	
	if not is_admin(ctx):
		await ctx.respond('You do not have permission to use this command', ephemeral=True, delete_after=10)
		return
 
 
	msg = f"Rebooting in {delay} minutes"
	await ctx.respond(msg)
	logger.info(msg)
	await asyncio.sleep(int(delay)*60)
 
	# function thread to initiate the reboot
	def reboot_helper(client:discord.Client, main_thread, exe, args):
		main_thread.join()			# wait for main thread to finish
		os.execv(exe, ['python3'] + args)
    
	reboot_thread = threading.Thread(target=reboot_helper, args=(client, threading.main_thread(), sys.executable, sys.argv))
	logger.info('Rebooting')
	reboot_thread.start()
	await client.close()


@client.slash_command(name='shutdown', description='Turns off the bot, must be restarted manually')
async def shutdown(ctx:discord.context.ApplicationContext):
	logger.debug('shutdown called')
	
	if not is_admin(ctx):
		await invalid_perm_response(ctx)
		return

	await ctx.respond('Shutting down')
	await client.close()
	sys.exit()


@client.slash_command(name='update_bot', description='Updates the bot from the github repo')
async def update_bot(ctx:discord.context.ApplicationContext):
	logger.debug('update_bot')
	
	if not is_admin(ctx):
		await invalid_perm_response(ctx)
		return

	msg = "Pulling from github"
	msg += f'\n```\n{os.popen("git pull").read()}\n```'

	await ctx.respond(msg)


@client.slash_command(name='dev_test', description='Tests the confirmation feature')
async def dev_test(ctx:discord.context.ApplicationContext):
    
	logger.debug('dev_test called')
    
	confirm = Confirmation('Test Confirmation')
	result = await confirm.get(ctx)
	await ctx.respond(f'Confirmation result: {result}', delete_after=10)


@client.slash_command(name='panic', description='Send a random panic gif')
async def panic(ctx: discord.context.ApplicationContext):
	panicGifs = getPanicGIFS()
	gif = panicGifs['GIFS'][random.randint(1, panicGifs['numGifs'])]
	await ctx.respond(gif)


@client.slash_command(name='nuke_chats', description='Nuke the chats')
async def nuke_chats(ctx: discord.context.ApplicationContext):
	logger.debug(f'nukeChats called by {ctx.author.name}')

	if not is_admin(ctx):
		await invalid_perm_response(ctx)
		return

	confirm = Confirmation('Erase all comments in #discussion, #lab, and #past-work channels')
	result = await confirm.get(ctx)

	if result:
		msg = f'Nuking chats - authorization: {get_user_info(ctx)}'
		logger.info(msg)
		await ctx.respond(msg)

		# Nuking part
		for channel in ctx.guild.channels:
			if ((channel.name == "discussion") or (channel.name == "lab") or (channel.name == "past-work")):
				await channel.delete()
		for cat in ctx.guild.categories:
			if "ECE" in cat.name:
				await cat.delete()
	
		# Rebuilding from ashes part
		for role in ctx.guild.roles:
			overwrites = {
				ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
				role: discord.PermissionOverwrite(read_messages=True)
			}

			if ("ECE" in role.name):
				category = await ctx.guild.create_category(role.name, overwrites=overwrites)
				await ctx.guild.create_text_channel("discussion", category=category, overwrites=overwrites)
				await ctx.guild.create_text_channel("past-work", category=category, overwrites=overwrites)
				if("/" in role.name):
					await ctx.guild.create_text_channel("lab", category=category, overwrites=overwrites)

@client.slash_command(name='clear_roles', description='Clear user roles.')
async def clear_roles(ctx: discord.context.ApplicationContext):
	logger.debug(f'clear_chats called by {ctx.author.name}')

	if not is_admin(ctx):
		await invalid_perm_response(ctx)
		return

	confirm = Confirmation(f'Clear all user roles besides admin and {persistent_roles}')
	result = await confirm.get(ctx)

	if result:
		msg = f'Clearing roles - authorization: {get_user_info(ctx)}'
		logger.info(msg)
		await ctx.respond(msg)

	rolesWithPersistence = []
	for role in persistent_roles:
		rolesWithPersistence.append(discord.utils.get(ctx.guild.roles, name=role))

	for member in ctx.guild.members:
		if (any(r in member.roles for r in rolesWithPersistence)):
			continue
		for role in member.roles:
			if (not (role.name in persistent_roles)):
				try:
					await member.remove_roles(role)
				except:
					print("Failed to remove role " + role.name + " from " + member.name)





# ----------------------- OLD COMMANDS BELOW ----------------------- 

@client.command()
async def testNewMemberMsg(ctx):
	await ctx.channel.send(NEWUSRMSG)