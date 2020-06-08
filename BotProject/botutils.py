import discord


def get_online_members(members):
	return [member for member in members if not member.bot and (
    		member.status == discord.Status.online or \
    		member.status == discord.Status.dnd)] 