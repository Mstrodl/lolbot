# -*- coding: utf-8 -*-

# the lolbot core
# (c) 2017 S Stewart under MIT License

import json
import logging
import random
import time
import traceback
# noinspection PyPackageRequirements
import aiohttp
# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands
# noinspection PyPackageRequirements
import utils.errors

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
description = '''Just a bot :)'''
exts = ['bots', 'donate', 'eval', 'fun', 'nekos', 'owner', 'stats', 'utility', 'weather', 'wa']


class Lul(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = json.load(open('config.json'))
        self.session = aiohttp.ClientSession()
        self.badarg = ['You need to put more info than this!', 'I didn\'t understan'
                                                               'd that.', 'Sorry, can\'t process that.',
                       'Read ' + self.config['prefix'] + 'help <command> for instructions.', 'Hmm?']
        # To be fair, we should record the init time after everything is ready
        self.init_time = time.time()

    async def on_ready(self):
        logging.info('lolbot - ready')
        # note that we use " instead of ' here
        # this is a limitation of the fstring parser
        await bot.change_presence(
            game=discord.Game(name=f'{self.config["prefix"]}help | v1.1', type=1, url='https://twitch.tv/monstercat'))
        logging.info('Playing status changed')

    async def on_command_error(self, ctx, error):
        not_ok = discord.utils.get(bot.emojis, name='notcheck')
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.message.add_reaction(not_ok)
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'Bad arg: `{random.choice(self.badarg)}`')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'Missing argument: {random.choice(self.badarg)}')
        elif isinstance(error, utils.errors.ServiceError):
            tb = ''.join(traceback.format_exception(
                type(error.original), error.original,
                error.original.__traceback__
            ))
            logging.error(f'Oops! {tb}')
            await ctx.message.add_reaction(not_ok)
            await ctx.send(f'Service error: `{tb}`')
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.message.add_reaction(not_ok)
            tb = ''.join(traceback.format_exception(
                type(error.original), error.original,
                error.original.__traceback__
            ))
            logging.error('A error occured.')
            logging.error(tb)


config = json.load(open('config.json'))
bot = Lul(command_prefix=config['prefix'], description=description, pm_help=None)

if __name__ == '__main__':
    for ext in exts:
        try:
            bot.load_extension(f'cogs.{ext}')
        except Exception:
            logging.error(f'Error while loading {ext}', exc_info=True)
        else:
            logging.info(f'Successfully loaded {ext}')

bot.run(config['token'])
