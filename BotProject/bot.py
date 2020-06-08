import random
import asyncio
from BotProject import utils
from discord.ext import commands
import logging

# setup logging
logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = 'NzE3NDcwNDM4NjA2NzY2MTIw.Xtaz1g.uiPCq9RYbhOfNzA3_KzukZa_Gec'
bot = commands.Bot(command_prefix='!')


@bot.command()
async def hello(ctx):
    is_owner = await bot.is_owner(ctx.message.author)
    if is_owner:
        await ctx.send('Здарова!')
    else:
        await ctx.send('Не борзей...')


@bot.command()
async def say(ctx, *args):
    members = ctx.message.guild.members
    member = None
    for m in members:
        if m.name == args[0]:
            member = m
            logger.debug(f'{member} and {member.name}')
            break
    if member is None:
        for m in members:
            if m.nick == args[0]:
                member = m
                logger.debug(f'{member} and {member.nick}')
                break
    _, *phrase = args
    if member:
        await ctx.send('{} {}'.format(member.mention, ' '.join(args)))
    else:
        await ctx.send(f'Данный pidor не найден')


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()


@bot.command()
async def flip(ctx):
    members = utils.get_online_members(ctx.message.guild.members)
    lucky_one = random.randint(0, len(members) - 1)

    await ctx.send('Выбираю лалку...')
    await asyncio.sleep(5)
    await ctx.send(f'Похоже {members[lucky_one].name} лалка)')


if __name__ == '__main__':
    bot.run(TOKEN)
