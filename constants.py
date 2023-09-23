from discord.ext import commands
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(_handler)

client = None               # type = commands.Bot, this should be overwriten by the main file


NEWUSRMSG = '''Welcome to the Easy Engineering server! If you have any questions regarding the server feel free to ask. Please read <#627273181778018344>. Remember we are all here to learn and help each other so be respectful to your fellow students. \nDISCLAIMER: This bot is in no way affiliated with Dr. Carnal or TNTECH in anyway.'''
RANDOM_MESSAGES_DAY = 2

channels = {
		'general': 627271589062508566,
		'C1-Q': 654556140415221776,
		'C2-Q': 654555766660792340,
}

# Roles to be kept when clearing roles
persistent_roles = [
    				"@everyone", 
                    "Admin", 
                    "Bots", 
                    "DarthCarnal", 
                    "YAGPDB.xyz", 
                    "Alumni", 
                    "Dumb Ass of the Day", 
                    "Professor", 
                    "Student", 
                    "IEEE Member", 
                    "Student", 
                    "ROLE LOCKED (Delinquent)", 
                    "The Random CS Student","Tau Beta Pi"
                    ]

messageTimes = []