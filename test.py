import discord
from discord.ext import *
import random
from db import DatabaseConnection
invite_dict = {}
db = DatabaseConnection()
class TestCog:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def bepis(self, ctx,member :discord.Member=None):
     a = ctx.author.name
     if ctx.author.nick != None:
         a = ctx.author.nick
     if not member:
         you = db.find_user(ctx.author.id)
         if not you:
             you = db.add_user(ctx.author.id, ctx.author.name)
         await ctx.send(a+ " has " + str(you['bepis']))
         return

     user = db.find_user(member.id)
     if not user:
         user = db.add_user(member.id,member.name)
     print(user)

     b = member.name
     if member.nick != None:
         b = member.nick
     await ctx.send(b +" Has " + str(user['bepis']) + " bepis left")


    @commands.command(pass_context=True)
    async def givebepis(self,ctx,member: discord.Member=None,message: int=None):
      if member is None or message is None:
          ctx.say("Error required arguments is missing or not in the correct format")
          return;
      user = db.find_user(member.id)
      print(message)
      if not user:
        user = db.add_user(member.id, member.name)
      currentBepis = int(user['bepis'])

      db.change_bepis(member.id,message+currentBepis)

    @commands.command(pass_context=True)
    async def pay(self,ctx,members:discord.Member,message:int):
        user = db.find_user(ctx.author.id)
        if message < 0:
            ctx.send("Nice try")
            return
        member = db.find_user(members.id)
        if not member:
            member = db.add_user(members.id,members.name)

        if not user:
            user = db.add_user(ctx.author.id, ctx.author.name)
        if members.id == ctx.author.id:
            await ctx.send("nice try")
            return
        currentBepis = int(user['bepis'])
        memberBepis= int(member['bepis'])
        if(currentBepis < message):
            await ctx.send("You dont have enough Bepis")
            return;
        db.change_bepis(ctx.author.id, currentBepis-message)
        db.change_bepis(members.id,memberBepis+message)
        a = user['bepis']
        await ctx.send("**Success you now have " + str(a-message) + " bepis left**")
    @commands.command(pass_context=True)
    async def invite(self,ctx):
        user = db.find_user(ctx.author.id)
        channel = self.bot.get_channel(ctx.channel.id)

        link = await channel.create_invite(max_uses=100)
        dic = dict({str(ctx.author.id):link.uses})
        if (invite_dict.get(str(ctx.author.id)) == None):
            invite_dict[str(ctx.author.id)] = link
            print("a")
        if(user['invites'].get(str(user['user_id'])) == None):
         print(user['invites'])
         user['invites'].update(dic)

         db.profiles.update_one({"user_id": user['user_id']}, {
            "$set": {"invites": user['invites']}
         })

         await ctx.send("Send this link to someone to get 30 bepis! " + link.url)
         return
        else:
            print("a")
            await ctx.send("Send this link to someone to get 30 bepis! " +list(invite_dict.values())[-1].code)
    @commands.command(pass_context=True)
    async def flip(self,ctx,amount:int,bepis:str):
        user = db.find_user(ctx.author.id)
        if amount > user['bepis']:
            await  ctx.send("nice try")
            return
        if bepis == "boopis" or bepis =="bepis":
            a = random.choice(["boopis","bepis"])
        if a == bepis:
            db.change_bepis(ctx.author.id,user['bepis']+amount*2)
            await ctx.send("You won! you now have " + str(user['bepis']+amount*2))
        else:
            db.change_bepis(ctx.author.id,user['bepis']-amount)
            await ctx.send("You Lost D: you now have " + str(user['bepis']-amount) )
def setup(bot):
    bot.add_cog(TestCog(bot))