import logging

from plugin import Plugin
import time
import logging
from datetime import datetime
import json

logger = logging.getLogger('discord')

class Logs(Plugin):
    now = datetime.now()
    dateTime = now.strftime("%Y-%m-%d %H.%M.%S")
    logFile = "Logs/DataHandler Log " + dateTime + ".log"
    isLogging = False

    fancy_name = "Logs"


    async def get_commands(self, guild):
        commands = [
            {
                'name': '!logs',
                'description': 'Get the server logs.'
            }
        ]
        return commands

    async def on_message(self, message):
        if(message.content=='!logs'):
            await self.darklai.send_message(
                    "Logs are currently saved clientside")


        now = datetime.utcnow()
        # Formating the msg
        author = message.author
        timestamp = time.mktime(message.timestamp.timetuple()) + message.timestamp.microsecond / 1E6
        msg = {
            "author":{
                    "id": author.id,
                    "name": author.name,
                    "discriminator": author.discriminator,
                    "avatar": author.avatar
                },
            "content": message.content,
            "clean_content": message.clean_content,
            "timestamp": timestamp,
            "attachments": message.attachments
        }
        date = now.strftime("%Y-%m-%d %H:%M:%S UTC")
        date = '{}-{}-{}'.format(now.year, now.month, now.day)
        channel = message.channel.name
        await self.log_message(0, msg)

    async def on_member_join(self, member):
        log = "{} {}#{} joined the server.".format(
            time.time(),
            member.name,
            member.discriminator
        )
        logger.info("{}#{} joined {}".format(
            member.name,
            member.discriminator,
            member.guild.name
        ))
        await self.log_message(log, 0)

    async def on_member_remove(self, member):
        log = "{} {}#{} left the server.".format(
            time.time(),
            member.name,
            member.discriminator
        )
        logger.info("{}#{} left {}".format(
            member.name,
            member.discriminator,
            member.guild.name
        ))
        await self.log_message(log, 0)

    async def on_member_ban(self, member):
        log = "{} {}#{} was banned from the server.".format(
                time.time(),
                member.name,
                member.discriminator
        )
        logger.info("{}#{} was banned from {}".format(
            member.name,
            member.discriminator,
            member.guild.name
        ))
        await self.log_message(log, 0)

    async def on_member_unban(self, guild, user):
        log = "{} {}#{} was unbanned from the server.".format(
                time.time(),
                user.name,
                user.discriminator
        )
        logger.info("{}#{} was unbanned from {}".format(
            user.name,
            user.discriminator,
            guild.name
        ))
        await self.log_message(log, 0)

    # Creates a new log message.
    # Will throw an exception if the logger receives an invalid string
    async def log_message(self, message, level):
        try:
            # If isLogging is set to true
            if self.isLogging:
                # If the level is set to 0, it is a debug message
                if level == 0:
                    logging.debug(str(message))

                # If the level is set to 1, it is a info message
                elif level == 1:
                    logging.info(str(message))

                # If the level is set to 2, it is a warning message
                elif level == 2:
                    logging.warning(str(message))

                # If the level is set to 3, it is a error message
                elif level == 3:
                    logging.error(str(message))

                # If the level is set to 4, it is a critical message
                elif level == 4:
                    logging.critical(str(message))

        # Handle any exceptions
        except Exception:
            # If isLogging is set to true
            if self.isLogging:
                # Define all of the local variables
                logging.critical('Message inputted for the log was invalid!')

            # Else, print out a error
            else:
                # Define all of the local variables
                print('ERROR: LOGGER CANNOT OUTPUT A CERTAIN MESSAGE.')
        # Define the endTime variable
        now = datetime.now()
        self.endTime = now
        return