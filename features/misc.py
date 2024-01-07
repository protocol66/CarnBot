import asyncio
from typing import Callable
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
  
  
class YesNoButtons(discord.ui.View):
	def __init__(self, yes_callback_fn:Callable, no_callback_fn:Callable):
		super().__init__()
  
		self.yes_callback_fn = yes_callback_fn
		self.no_callback_fn = no_callback_fn

	@discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
	async def yes_callback_wrapper(self, button: discord.ui.Button, interaction: discord.Interaction):
		await self.yes_callback_fn(button, interaction)

	@discord.ui.button(label="No", style=discord.ButtonStyle.red)
	async def no_callback_wrapper(self, button: discord.ui.Button, interaction: discord.Interaction):
		await self.no_callback_fn(button, interaction)
	

class Confirmation(YesNoButtons):
	def __init__(self, action:str, timeout:int=10, default=False):
		super().__init__(self.yes, self.no)
  
		self.conf_msg = f'This will **{action}**\nAre you sure you want to do this?'
		self.timeout = timeout
		self.sent_interaction = None
		self.result = None
		self.result_event = asyncio.Event()
		self.default_choice = default

	async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
		logger.debug('yes_callback_fn called')
		self.result = True
		self.result_event.set()
		await interaction.response.send_message('Confirmed', ephemeral=False)

	async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
		logger.debug('no_callback_fn called')
		self.result = False
		self.result_event.set()
		await interaction.response.send_message('Cancelled', ephemeral=True, delete_after=self.timeout)
		await asyncio.sleep(self.timeout)
		await self.sent_interaction.delete_original_message()
  
	async def get(self, ctx:discord.context.ApplicationContext):
		logger.debug(f'get_confirmation called from {ctx.author}')
  
		self.result_event.clear()
		self.result = None
		self.sent_interaction = await ctx.respond(self.conf_msg, view=self, ephemeral=True)
	
		try:
			await asyncio.wait_for(self.result_event.wait(), timeout=self.timeout)
		except asyncio.TimeoutError:
			logger.debug('Confirmation timed out')
			self.result = self.default_choice
			await self.sent_interaction.delete_original_message()

		return self.result