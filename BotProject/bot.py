import random
import asyncio
import botutils
from discord.ext import commands
import logging
import configparser
import newsparser

# setup logging
logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def read_config():
    """
    read config from file
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['discord'].get('token')


TOKEN = read_config()
news_parser = newsparser.IgromaniaNewsParser('key.txt')


class Registrar(type):
    def __new__(cls, name, bases, dictr):
        commands_ = []
        for k, v in dictr.items():
            if isinstance(v, commands.core.Command):
                commands_.append(v)
        dictr['commands_'] = commands_
        return type.__new__(cls, name, bases, dictr)


class BotClient(commands.Bot, metaclass=Registrar):
    def register_commands_(self):
        for func in BotClient.commands_:
            self.add_command(func)


    @commands.command()
    async def hello(ctx):
        is_owner = await bot.is_owner(ctx.message.author)
        if is_owner:
            await ctx.send('Здарова!')
        else:
            await ctx.send('Не борзей...')


    @commands.command()
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
            await ctx.send(f'Данный пользователь не найден')


    @commands.command()
    @commands.is_owner()
    async def shutdown(ctx):
        await ctx.bot.logout()


    @commands.command()
    async def flip(ctx):
        members = botutils.get_online_members(ctx.message.guild.members)
        lucky_one = random.randint(0, len(members) - 1)

        await ctx.send('Выбираю лалку...')
        await asyncio.sleep(5)
        await ctx.send(f'Похоже {members[lucky_one].name} лалка)')


    @commands.command()
    async def news(ctx):
        is_owner = await bot.is_owner(ctx.message.author)
        if is_owner:
            bot.loop.create_task(BotClient.task_news(ctx))
        else:
            await ctx.send('Нет доступа.')


    async def task_news(ctx):
        logger.debug('Here')
        while True:
            news = news_parser.parse_news()
            logger.debug('Exploring news...')
            for news_element in news:
                await ctx.send(
                    news_parser.site_url + news_element.a.get('href'))
            await asyncio.sleep(1800)


if __name__ == '__main__':
    bot = BotClient(command_prefix='!')
    bot.register_commands_()
    bot.run(TOKEN)
