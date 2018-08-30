import discord
from discord.ext import commands
import random
from db import DatabaseConnection
import math
db = DatabaseConnection()

embed = discord.Embed

class ShibeCog:

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def catch(self,ctx):
     member = ctx.author
     channel = self.bot.get_channel(445754950853853184)
     shibess = []
     user = db.find_user(member.id)
     if not user:
         user = db.add_user(member.id, member.name)
     async for message in channel.history():
         shibess.append(message.content.split(' ',1))
     print(shibess)
     for letter in shibess:
         if letter == []:
            shibess.remove(letter)

     a = random.choice(shibess)
     b = a[1]
     url = ""
     for pic in shibess:
         if pic[1] == b:
             url = pic[0]
             break
     embed = discord.Embed(title="You Caught a " +b + " Congratulations!!!!!")
     embed.set_image(url=url)
     await ctx.send(embed=embed)
     inventory = user['inventory']['Shibes']['name']
     z = len(inventory)+1

     inventory.update({str(z):b})
     db.profiles.update_one({"user_id": user['user_id']}, {
      "$set": {"inventory": user['inventory']}
     })

    @commands.command(pass_context=True)
    async def inv(self,ctx,page_num:int=None):
         member = ctx.author
         user = db.find_user(member.id)
         shibe = []
         amount = 1
         length = 0
         page = 0;

         shibes = []
         boop =int(float(len(shibes) / 20))
         footer = str(page+1) + "/" + str(boop+1)

         try:
             length  = len(user['inventory']['Shibes']['name'])
             print(length)
         except:
             pass
         if (length == 0):
             embed = discord.Embed(title="Error", description="You dont have any shibes")
             await ctx.send(embed=embed)
         if not user:
             user = db.add_user(member.id, member.name)
         for shibea in user['inventory']['Shibes']['name'].values():
             shibes.append(shibea)
         if page_num!= None:
             page+=page_num-1
             page=page*20
             footer = str(page_num) + "/" + str(int((len(shibes) / 20 + 1)))
         if page > len(shibes):
             embed = discord.Embed(title='Error',description='You dont have that many Shibes')
             await ctx.send(embed=embed)
             return
         for num in range(page, page + 20, 1):
             try:
              shibe.append(str(num+1)+")" + shibes[num] + '\n')
             except:
              break
         embed = discord.Embed(title='Shibes', description=''.join(shibe))
         embed.set_footer(text=footer)
         await ctx.send(embed=embed)
    @commands.command(pass_context=True)
    async def show(self,ctx,message: int=None):
        channel = self.bot.get_channel(445754950853853184)
        shibess = []
        if message is None:
            embed = discord.Embed(title="Error", description="You neglected to enter a number")
            await ctx.send(embed=embed)
            return
        user = db.find_user(ctx.author.id)
        if not user:
            embed = discord.Embed(title="Error", description="You have no shibes please go use catch")
            await ctx.send(embed=embed)
            return
        async for messages in channel.history():
            shibess.append(messages.content.split(' ', 1))
        length = len(user['inventory']['Shibes']['name'])
        url = ""

        shibe = user['inventory']['Shibes']['name'].get(str(message))
        print(shibe)
        if(message > length):
            embed = discord.Embed(title="Error", description="You don't have that many shibes")
            await ctx.send(embed=embed)
            return
        if (shibe.find(" *(") != 0 and shibe.find("*)") != 0):
            print("a")
            shibea = shibe[shibe.find("*(") + 2:shibe.find(")*")]

        for pic in shibess:
            if pic[1] == shibea:
                shibe = shibea
                url = pic[0]
                break
        if url == "":
            for pic in shibess:
                if pic[1] == shibe:
                    url = pic[0]
                    break

        print(url)
        embed = discord.Embed(title=shibe,description="Showing "+shibe)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def shibe(self, ctx):
        channel = self.bot.get_channel(442853085639868417)
        shibes = []
        async for message in channel.history():
             shibes.append(message.attachments)
        a = random.choice(shibes)
        try:
         b = a[0].url
         embed = discord.Embed(title="Shibe!!")
         embed.set_image(url=b)
         await ctx.send(embed=embed)
        except:
           await self.shibe.callback(self,ctx)

    @commands.command(pass_context=True)
    async def sell(self, ctx, message: int = None):
        shibess = []
        if message is None:
            ctx.send("Oi input a number please")
            return
        user = db.find_user(ctx.author.id)
        if not user:
            ctx.send("You have no shibes to show please  use !catch")
            return
        del user['inventory']['Shibes']['name'][str(message)]
        await ctx.send("You now have " + str(user['bepis']+10) + " Bepis!")
        db.change_bepis(user['user_id'],user['bepis']+10)
        db.profiles.update_one({"user_id": user['user_id']}, {
            "$set": {"inventory": user['inventory']}
        })

    @commands.command(pass_context=True)
    async def brag(self,ctx,message:int):
         await self.show.callback(self,ctx,message)

    @commands.command(pass_context=True)
    async def nickshibe(self, ctx, message: int = None,*, nick: str):
        shibess = []
        if message is None:
            ctx.send("Oi input a number please")
            return
        user = db.find_user(ctx.author.id)
        inventory = user['inventory']['Shibes']['name']
        shibe = inventory.get(str(message))
        if("*(" in shibe ):
            shibe = shibe[shibe.find("*(")+2:shibe.find(")*")]

        inventory.update({str(message): nick + " *(" + shibe + ")*"})
        embed = discord.Embed(title="New Nickname",description="Your new Shibes nick is "+ nick)
        await ctx.send(embed=embed)
        db.profiles.update_one({"user_id": user['user_id']}, {
            "$set": {"inventory": user['inventory']}
        })

    @commands.command(pass_context=True)
    async def resetnick(self,ctx,message:int):
        user = db.find_user(ctx.author.id)
        inventory = user['inventory']['Shibes']['name']
        shibe = inventory.get(str(message))
        if(shibe.find("*(") != 0):

            shibe = shibe[shibe.find("*(")+2:shibe.find(")*")]
            await ctx.send(shibe + " Nickname has been reset")
        inventory.update({str(message) : shibe})
        db.profiles.update_one({"user_id": user['user_id']}, {
            "$set": {"inventory": user['inventory']}
        })

    @commands.command(pass_context=True)
    async def shop(self, ctx, shopp: int = None):
        test = ctx.author
        user = db.find_user(ctx.author.id)
        channel = self.bot.get_channel(445754950853853184)
        shibes = []
        amount = 1
        async for message in channel.history():
            shibes.append(message.content.split(' ', 1))
        print(shibes)
        arr = []
        shop = []
        for listt in shibes:
            print(listt)
            shop.append((str(amount) + " " + listt[1] + '\n'))
            arr.append(listt[1])
            amount += 1

        if shopp == None:

            embed = discord.Embed(title="Available Shibes",description=''.join(shop))
            await test.send(embed=embed)
        elif(shopp < len(shibes)+1 and user['bepis'] > 20):

            await test.send("You have bought" + arr[shopp-1])
            db.change_bepis(user['user_id'],user['bepis']-20)
            await test.send("You have " + str(user['bepis']-20))
            inventory = user['inventory']['Shibes']['name']
            z = len(inventory) + 1

            inventory.update({str(z): arr[shopp-1]})
            db.profiles.update_one({"user_id": user['user_id']}, {
                "$set": {"inventory": user['inventory']}
            })
        else:
            embed = discord.Embed(title="Error",description="You don't have enough bepis or that is an invalid shibe")
            await ctx.send(embed=embed)
            return

def setup(bot):
    bot.add_cog(ShibeCog(bot))
