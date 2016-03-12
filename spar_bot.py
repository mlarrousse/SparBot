import discord
from lib import db
from lib.fight import Fight
bot = discord.Client()
bot.login("a.spilt.fish@gmail.com", "pandas")


def please_register_first(channel, author):
    bot.send_message(channel, "Sorry, {name}, Please register first.".format(name=author))


@bot.event
def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!help'):
        bot.send_message(message.channel, "**!register <character name>**\n\t Signs up for Sparring. \n"
                                          "**!help** \n\t Displays this message. \n")

    if message.content.startswith('!register'):
        if db.user_is_registered(message.author):
            character_name = db.get_character_name(message.author)
            bot.send_message(message.channel, "User {username} is already registered with character {character_name}.".
                             format(username=message.author, character_name=character_name))
        elif (message.content.split(' ')[1] == 'help') or (not message.content.split(' ')[1]):
            "Command Syntax: !register <character name>"
        elif message.content.split(' ')[1]:
            bot.send_message(message.channel, 'Welcome to Sparring, {character_name}!'.
                             format(character_name=message.content.split(' ')[1]))
            db.register_user(message.author, message.content.split(' ')[1])

    if message.content.startswith('!train'):
        if db.user_is_registered(message.author):
            Fight(message.author, "scarecrow")

    if message.content.startswith('!stats'):
        if db.user_is_registered(message.author):
            pass #get character stats
        else:
            please_register_first(message.channel, message.author)



bot.run()
