import discord
from discord.ext import commands
import json as      json
import time
from decimal import *
import json
import datetime


msgs = {}
login = time.time()
times = []
memeBank = []
loaded = []
buxmemeoji = "<:memeBUX:380510554349109249>"
loggedIn = time.time()


class timestamps:
    def __init__(self, id,  online = None, voiceOnline = None):
        self.id = id
        self.online = online
        self.voiceOnline = voiceOnline
        self.totalOnline = 0
        self.totalVoiceOnline = 0
        self.messages = 0
        self.totalMessages = 0

    def __eq__(self, other):
        return self.id == other



class user:
    def __init__(self, name, id, memeBUX: Decimal):
        self.name = name
        self.id = id
        self.memeBUX = memeBUX

    def __eq__(self, other):
        return self.id == other

class memebux:

    try:
        loaded = json.load(open("cogs\\bank.json", "r"))
        for x in loaded:
            x['memeBUX'] = Decimal(x['memeBUX'])
            memeBank.append(user(*list(x.values())))
    except json.decoder.JSONDecodeError:
        pass

    def __init__(self, bot):
        self.bot = bot

    def format(self, number):
        return Decimal(number).quantize(Decimal('0.00'), rounding = ROUND_UP)

    def searchForTimestamp(self, id):
        for i in range(len(times)):
            if times[i] == id:
                return i
        return -1

    def searchForUser(self, id):
        for i in range(len(memeBank)):
            if memeBank[i] == id:
                return i
        return -1

    def inLoaded(self, list):
        for x in loaded:
            if x['id'] == list['id']:
                return True
        return False

    def resetMessageCounts(self):
        for x in times:
            x.totalMessages = 0
            x.messages = 0

    def save(self):
        global loaded
        try:
            loaded = json.load(open("cogs\\bank.json", "r"))
        except json.decoder.JSONDecodeError:
            pass
        for x in memeBank:
            copy = x.__dict__.copy()
            copy['memeBUX'] = str(copy['memeBUX'])
            if loaded and self.inLoaded(copy):
                for i in range(len(loaded)):
                    if loaded[i]['id'] == copy['id']:
                        loaded.__setitem__(i, copy)
            else:
                loaded.append(copy)
        with open("cogs\\bank.json", "w") as f:
            json.dump(loaded, f, indent = 2)


    async def checkBalance(self, id, amount):
        if self.searchForUser(id) == -1:
            await self.bot.say("can u pls fucking make an account first like how tf do you expect to make a transaction if u don't even have an account?!?!\n\n{}".format(buxmemeoji))
            return False
        if memeBank[self.searchForUser(id)].memeBUX >= self.format(amount):
            return True
        else:
            await self.bot.say("LOL ur too fking poor literally only has {} memeBUX fking kys kek\n\n{}".format(memeBank[self.searchForUser(id)].memeBUX, buxmemeoji))

    @commands.command(pass_context = True)
    async def timeleft(self, ctx):
        await self.bot.say("{} seconds until message counts reset".format(time.time() - loggedIn))

    @commands.command(pass_context = True)
    async def adduser(self, ctx):
        if self.searchForUser(ctx.message.author.id) == -1:
            memeBank.append(user(ctx.message.author.name,ctx.message.author.id, self.format(0)))
            self.save()
            await self.bot.say("ayo cunt your fucking id is {} write it down on a piece of flipping origami paper u faggot\n\n{}".format(ctx.message.author.id,buxmemeoji))
        else:
            await self.bot.say("ur hella gay how tf u gon try to make 2 accounts u little faggot go get a better brain\n\n{}".format(buxmemeoji))

    @commands.command(pass_context = True)
    async def balance(self, ctx):
        if self.searchForUser(ctx.message.author.id) == -1:
            await self.bot.say("please go to the teller to make a fucking account you dumb shit holy aids\n\n{}".format(buxmemeoji))
        else:
            await self.bot.say("ur balance is literally only {} memeBUX lmfao xd ur hella shit nd will never amount to anything\n\n{}".format(memeBank[self.searchForUser(ctx.message.author.id)].memeBUX, buxmemeoji))

    @commands.command(pass_context = True)
    async def give(self, ctx, user : discord.User, amount : float):
        amount = self.format(amount)
        if await self.checkBalance(ctx.message.author.id, amount) and self.searchForUser(user.id) != -1:
            memeBank[self.searchForUser(user.id)].memeBUX += amount
            memeBank[self.searchForUser(ctx.message.author.id)].memeBUX -= amount
            self.save()
            await self.bot.say("**{}** gave **{}** {} memeBUX\n\n{}".format(ctx.message.author.display_name, user.display_name, amount, buxmemeoji))

    @commands.command(pass_context = True)
    async def add(self, ctx, amount : int):
        if self.searchForUser(ctx.message.author.id) == -1:
            await self.bot.say("acc dont exist vroski\n\n{}".format(buxmemeoji))
        else:
            memeBank[self.searchForUser(ctx.message.author.id)].memeBUX += amount
            self.save()
            await self.bot.say("just added {} memeBUX to {} dont spend it all on one meme\n\n{}".format(amount, ctx.message.author.display_name, buxmemeoji))

    @commands.command(pass_context = True)
    async def getpaid(self, ctx):
        global loggedIn
        i = self.searchForTimestamp(ctx.message.author.id)
        u = self.searchForUser(ctx.message.author.id)
        payment = 0
        paymentVoice = 0
        paymentMessages = 0
        onlineTime = 0
        voiceTime = 0
        messages = 0
        if time.time() - loggedIn > 60:
            self.resetMessageCounts()
            loggedIn += 60
        msgs[ctx.message.id] = True
        times[i].messages += 1
        if times[i].online is not None: #if a time stamp exists then add any time they had before to the time in this current session and reset the timestamp
            onlineTime = times[i].totalOnline + (time.time() - times[i].online)
            payment = self.format(onlineTime * (1/3150))
            memeBank[u].memeBUX += payment
            times[i].totalOnline = 0
            times[i].online = time.time()


        else:#if no time stamp exists then they must either have already left before or never been online
            onlineTime = times[i].totalOnline
            payment = self.format(onlineTime * (1 / 3150))
            memeBank[u].memeBUX += payment
            times[i].totalOnline = 0

        if times[i].voiceOnline is not None:
            voiceTime = times[i].totalVoiceOnline + (time.time() - times[i].voiceOnline)
            paymentVoice = self.format(voiceTime * (1/3600))
            memeBank[u].memeBUX += paymentVoice
            times[i].totalVoiceOnline = 0
            times[i].voiceOnline = time.time()

        else:
            voiceTime = times[i].totalVoiceOnline
            paymentVoice = self.format(voiceTime * (1 / 3600))
            memeBank[u].memeBUX += paymentVoice
            times[i].totalVoiceOnline = 0

        if times[i].totalMessages < 20:
            if times[i].messages + times[i].totalMessages > 20:
                times[i].messages = 20 - times[i].totalMessages
            times[i].totalMessages += times[i].messages
            messages = times[i].messages
            print("messages:{}".format(messages))
            paymentMessages = self.format(messages * (1/50))
            memeBank[u].memeBUX += paymentMessages
            times[i].messages = 0
            print(times[i].totalMessages)
        self.save()
        await self.bot.say("you just got {} memeBUX for being online for {} seconds, being in voice for {} seconds, and sending {} messages\n\n{}".format(payment + paymentVoice + paymentMessages, onlineTime, voiceTime, messages, buxmemeoji))


    async def on_ready(self):
        for member in self.bot.get_server('285130380603031562').members:
            if member.status is not discord.Status.offline:
                print(member.display_name)
                if member.voice_channel is not None:
                    times.append(timestamps(member.id, time.time(), time.time()))
                else:
                    times.append(timestamps(member.id, time.time()))
            else:
                times.append(timestamps(member.id))

    async def on_member_update(self, before, after):
        if before.status is discord.Status.offline and after.status is not discord.Status.offline:
            times[self.searchForTimestamp(after.id)].online = time.time()
        if before.status is not discord.Status.offline and after.status is discord.Status.offline:
            times[self.searchForTimestamp(after.id)].totalOnline =  time.time() - times[self.searchForTimestamp(after.id)].online
            times[self.searchForTimestamp(after.id)].online = None

    async def on_voice_state_update(self, before, after):
        if before.voice_channel is None and after.voice_channel is not None:
            times[self.searchForTimestamp(after.id)].voiceOnline = time.time()
        if before.voice_channel is not None and after.voice_channel is None:
            times[self.searchForTimestamp(after.id)].totalVoiceOnline = time.time() - times[self.searchForTimestamp(after.id)].voiceOnline
            times[self.searchForTimestamp(after.id)].voiceOnline = None

    async def on_message(self, msg):
        if self.searchForUser(msg.author.id) != -1:
            if msgs.get(msg.id, False) == False:
                print(msg.content)
                times[self.searchForTimestamp(msg.author.id)].messages += 1
                print("msgs {}".format(times[self.searchForTimestamp(msg.author.id)].messages))






def setup(bot):
    bot.add_cog(memebux(bot))


