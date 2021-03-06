import asyncio
import sys
import time
import json
# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands
from random import choice as rchoice

config = json.load(open('config.json'))
GitError = 'fatal: Not a git repository (or any of the parent directories): .git'
NoCommit = '*No commit'
NoRelease = '*No release*'

async def is_bot(u: discord.Member):
    if u.bot:
        return 'Yep!'
    else:
        return 'Nope.'

async def get_nick(u: discord.Member):
    if u.nick:
        return u.nick
    else:
        return '*None*'


async def get_game_name(u: discord.Member):
    if u.game:
        return u.game.name
    else:
        return '*None*'


async def get_join_date(u: discord.Member):
    meme = u.joined_at
    date = meme.strftime('%b %d, %Y %H:%M:%S')
    return date


async def get_status(u: discord.Member):
    if u.status == discord.Status.online:
        return 'Online'
    elif u.status == discord.Status.idle:
        return 'Idle'
    elif u.status == discord.Status.dnd or discord.Status.do_not_disturb:
        return 'Do not disturb'
    elif u.status == discord.Status.offline:
        return 'Offline/invisible'


class Etc:
    def __init__(self, bot):
        self.bot = bot
        self.support = 'https://discord.gg/PEW4wx9'

    @commands.command()
    async def uptime(self, ctx):
        """Shows uptime of lolbot"""
        # Thanks Luna you make good code lul
        sec = round(time.time() - self.bot.init_time)
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        upEm = discord.Embed(title='Uptime', colour=0x690E8)
        startedOn = time.strftime('%b %d, %Y %H:%M:%S', time.localtime(self.bot.init_time))
        upEm.add_field(name='Started on', value=startedOn, inline=False)
        upEm.add_field(name='Uptime', value=f' {d} days, {h} hours, {m} minutes and {s} seconds', inline=False)
        await ctx.send(embed=upEm)

    @commands.command()
    async def ping(self, ctx):
        """Well... you know this"""
        one = time.monotonic()
        a = await ctx.send('wew dude')
        two = time.monotonic()
        ms = round((two - one) * 1000, 2)
        gw = round(self.bot.latency * 1000)
        meme = discord.Embed(title='Pong!', colour=0x690E8)
        meme.add_field(name='Normal ping', value=f'**{ms}**ms')
        meme.add_field(name='Gateway ping', value=f'**{gw}**ms')
        await a.delete()
        await ctx.send(embed=meme)

    @commands.command()
    async def stats(self, ctx):
        """A few stats."""
        statInfo = await ctx.bot.application_info()
        statEmbed = discord.Embed(title='Stats', description='This bot is'
                                                             ' powered by [lolbot](https://github.com/tilda/lolbot), a fast and powerful '
                                                             'Python bot.', colour=0x690E8)
        statEmbed.add_field(name='Owner', value=statInfo.owner.mention + '('
                                                + str(statInfo.owner) + ' - ID: ' + str(statInfo.owner.id) + ')')
        statEmbed.add_field(name='Python', value=sys.version)
        statEmbed.add_field(name='discord.py', value=discord.__version__)
        statEmbed.add_field(name='Servers', value=f'{len(self.bot.guilds)}')
        statPool = ['What have you done now?', 'Why should I do this again?', 'Oh..',
                    'Where did the RAM go?', 'grumble grumble', 'Please hold.', 'No, just, no.',
                    'Have you tried rebooting?', 'memework makes the dreamwork!']
        statEmbed.set_footer(text=rchoice(statPool))
        await ctx.send(embed=statEmbed)

    @commands.command()
    async def invite(self, ctx):
        """Gives a invite for the bot (and also the official server)"""
        info = await ctx.bot.application_info()
        invEmb = discord.Embed(colour=0x690E8)
        invEmb.add_field(name='Invite lolbot', value='[Click here]'
                                                     '(' + discord.utils.oauth_url(info.id) + ')')
        invEmb.add_field(name='Official server', value=str(self.support))
        await ctx.send(embed=invEmb)

    @commands.command(aliases=['userinfo', 'uinfo'])
    async def user(self, ctx, u: discord.Member):
        try:
            status = await get_status(u)
            join_date = await get_join_date(u)
            game = await get_game_name(u)
            nick = await get_nick(u)
            bot = await is_bot(u)
        except Exception as e:
            raise commands.CommandInvokeError(f'oops: {e}')

        e = discord.Embed(colour=0x690E8)
        e.add_field(name='Name', value=u.name)
        e.add_field(name='Status', value=status)
        e.add_field(name='Joined at', value=join_date)
        e.add_field(name='Currently playing', value=game)
        e.add_field(name='Nickname', value=nick)
        e.add_field(name='Is bot', value=bot)
        await ctx.send(embed=e)

    @commands.command()
    async def version(self, ctx):
        """Returns current version of lolbot"""
        with ctx.typing():
            tag = await asyncio.create_subprocess_shell('git describe --abbrev=0 --tags',
                                                        stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE)
            commit = await asyncio.create_subprocess_shell('git log --oneline --abbrev=2',
                                                           stdout=asyncio.subprocess.PIPE,
                                                           stderr=asyncio.subprocess.PIPE)
            co, ce = map(lambda s: s.decode('utf-8'), await commit.communicate())
            to, te = map(lambda st: st.decode('utf-8'), await tag.communicate())
            if GitError in f'{co}{ce}':
                co = NoCommit
                ce = None
            else:
                pass
            if GitError in f'{to}{te}':
                to = NoRelease
                te = None
            else:
                pass
            if ce and te is None:
                runVal = '*no release*'
                rVal0 = '*no tag*'
            else:
                runVal = co
                rVal0 = to
            e = discord.Embed(colour=0x690E8)
            e.add_field(name='Latest tag', value=rVal0)
            e.add_field(name='Currently running', value=runVal)
            e.set_footer(text='powered by git (and stuff)!')
            await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Etc(bot))
