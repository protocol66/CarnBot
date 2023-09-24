import discord
import asyncio
import random
import sys
import os

from constants import client, persistent_roles, channels, NEWUSRMSG
from .utils import create_logger, getDates, getPanicGIFS

logger = create_logger('commands')

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
async def tbp(ctx, *arg):
	for line in arg:
		user = ctx.guild.get_member_named(line)
		role = discord.utils.get(user.guild.roles, name="Tau Beta Pi")
		await user.add_roles(role)



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
	await ctx.send('I am designed to give some amusement, annoyance, and on rare occasions help to all jedi (EE/CompE) in training\n*I am in no way affiliated with Dr. Charles Carnal*')


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
	await ctx.send(os.popen("git pull").read())
	#its working

@client.command()
async def panic(ctx):
	panicGifs = getPanicGIFS()
	gif = panicGifs['GIFS'][random.randint(1, panicGifs['numGifs'])]
	await ctx.channel.send(gif)


@client.command()
async def testNewMemberMsg(ctx):
	await ctx.channel.send(NEWUSRMSG)

@client.command()
async def nukeChats(ctx):
	for channel in ctx.guild.channels:
		if ((channel.name == "discussion") or (channel.name == "lab") or (channel.name == "past-work")):
			await channel.clone()
			await channel.delete()

@client.command()
async def clearRoles(ctx):
    for member in ctx.guild.members:
        for role in member.roles:
            if (not (role.name in persistent_roles)):
                try:
                    await member.remove_roles(role)
                except:
                    logger.error("Failed to remove role " + role.name + " from " + member.name)

