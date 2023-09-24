import discord
from datetime import datetime, timedelta
import random

from constants import client
from .utils import create_logger

logger = create_logger('misc')

async def dumbAssOfTheDay():
	while True:
		randMem = random.choice(list(client.get_all_members()))
		logger.info(f"DAD is {randMem}")
		role = discord.utils.get(randMem.guild.roles, name="Dumb Ass of the Day")
		for mem in role.members:
			await mem.remove_roles(role)
		await randMem.add_roles(role)

		now = datetime.today() + timedelta(days=1)
		resetTime =  now.replace(hour=14, minute=0)
		await discord.utils.sleep_until(resetTime)
		# sleep(10)
		await randMem.remove_roles(role)