import discord
from discord.ext import commands

import asyncio
import random
from datetime import datetime, timedelta
import pickle


from constants import client, RANDOM_MESSAGES_DAY
from .utils import getDates, getPanicGIFS, getQuotes



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


async def important_reminders(channels: dict):
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


# well I have code this about 4 times, feel free to make fun
async def random_quote(channels: dict):
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

			now = datetime.today() + timedelta(days=1)
			# hour = 14 because the bot uses UTC time
			resetTime = now.replace(hour=14, minute=0)
			await discord.utils.sleep_until(resetTime)

		elif (nowDec < 8):
			now = datetime.today()
			# hour = 14 because the bot uses UTC time
			resetTime = now.replace(hour=14, minute=0)
			await discord.utils.sleep_until(resetTime)

		else:
			now = datetime.today() + timedelta(days=1)
			# hour = 14 because the bot uses UTC time
			resetTime = now.replace(hour=14, minute=0)
			await discord.utils.sleep_until(resetTime)
