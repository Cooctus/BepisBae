import discord
import os
from discord.ext import commands
from db import DatabaseConnection
import random
invite_dict = {}

bot = commands.Bot(command_prefix='-',description='a')
extensions = ['shibe',
              'test'
              ]


db = DatabaseConnection()
@bot.event
async def on_ready():
        print('Logged on as {0}!'.format(bot.user))

@bot.event
async def on_member_join(member: discord.Member):

    db = DatabaseConnection()

    user = db.find_user(member.id)
    if not user:
        user = db.add_user(member.id,member.name)




    try:
     await member.send("""
    Welcome to the cult """ + member.name + """
----------------------------------------------------------------------
**Here's some stuff you should know**

- A shiba inu is a type of dog, but you can call it by several different names, including shibe, shober, doge, shobe, shib, etc. To see a random pic of a shibe, you can do !shibe. 

- A baby shibe is known as a potat. Why? Because they look like little potatoes!

- There are several different drinks that shibes drink (it's sort of a meme, don't question our ways). All you need to know is that Bepis is the best drink, and Conk is the worst. There is a video in #important explaining the drinks. Bepis is also the currency of the server. :bepisbot: 

- Common "server slang/purposeful misspellings": mlem (lick), fren (friend), and happ (happy). If a word ends in the "ck" sound, we make it end in "cc" sometimes, like "thicc", "licc", and "drincc". I know it may seem cringey but thats the way things are.

- For a list of roles, rules, bot commands, and some other cool stuff read #important. To know more about a channel, read that channel's topic. If you have any questions, feel free to ask anyone.

Now GET OUT THERE and have fun! 
""")
    except:
        pass
    channel = bot.get_channel(484129483335663620)
    await channel.send("Welcome to the Shibe Cult "+ member.name)
    invites = member.guild.members
    invites2 = await member.guild.invites()
    from test import invite_dict
    print(invite_dict)

    for test in invites2:
        for value,key in invite_dict.items():

          
            if(test.code == key.code and test.uses > key.uses):
             user2 = db.find_user(int(value))
             db.change_bepis(user2['user_id'],user2['bepis']+30)
             db.change_bepis(user['user_id'],user['bepis']+20)
             await channel.send(member.name + " Has earned 20 bepis for using "+ user2['username'] + "'s Refferal Link")
             break;





if __name__ == '__main__':

    for extension in extensions:
            try:
                bot.load_extension(extension)

            except (discord.ClientException, ModuleNotFoundError):
                 print(f'Failed to load extension {extension}.')

    bot.run('')

