import discord      # pip3 install discord.py
import asyncio
import giphypop     # pip3 install giphypop
from discord import Game, Embed, Color, Status, ChannelType
from discord.ext import commands
from os import path
import time
import datetime

GIPHY_TOKEN = "" #the token here
PREFIX = "\\"


# Here you can define which message invokes should be automatically replced
REPLACES = {
    "-lenny-": "( ͡° ͜ʖ ͡°)",
    "-meh-": "¯\_(ツ)_/¯",
    "-wut-": "ಠ_ಠ",
    "-yeah-": "(⌐■_■)",
    "-tt-": "(╯°□°）╯︵ ┻━┻",
    "-give-": "༼ つ ◕_◕ ༽つ",
    "-yay-": "( ﾟヮﾟ)",
    "-smile-": "{◕ ◡ ◕}",
    "-wizard-": "(∩´• . •`)⊃━☆ﾟ.*",
    "--": "",
}

""" 
    ['wizard', '(∩´• . •`)⊃━☆ﾟ.*'],
    ['happy', '╰( ◕ ᗜ ◕ )╯'],
    ['party', '(つ°ヮ°)つ'],
    ['dance', '└╏ ･ ᗜ ･ ╏┐'],
    ['disco', '（〜^∇^)〜'],
    ['woahmagic', '(∩｡･ｏ･｡)っ.ﾟ☆`｡'],
    ['rage', '(┛ಠДಠ)┛彡┻━┻'],
    ['excited', '☆*:. o(≧▽≦)o .:*☆'],
    ['music', '(✿ ◕ᗜ◕)━♫.*･｡ﾟ'],
    ['woah', '【 º □ º 】'],
    ['flipparty', '༼ノ◕ヮ◕༽ノ︵┻━┻'],
    ['sad', '(;﹏;)'],
    ['wink', '(^_-)']
"""

# Creating selfbot instance
bot = commands.Bot(command_prefix=PREFIX, description="''Selfbot by AbbestiaDC''", self_bot=False)

#==================================
#PERIODIC MESSAGE SEND


channel = None

async def periodic():
    global channel
    while True:
        await bot.send_message(channel,".timely")
        print('periodic')
        await asyncio.sleep(3602) #time in seconds to send the command

#stop command not completed, i need a class
# def stop():
#     task.cancel()


@bot.event
async def on_ready():

    print(
            "\n +--------------------------------------------+"
            "\n |        AbbestiaDC - discord self-bot       |"
            "\n |        (c) 2019 Simone PP Very Long        |"
            "\n +--------------------------------------------+\n"
         )
    print("Logged in as %s#%s" % (bot.user.name, bot.user.discriminator))
    print("ID: " + bot.user.id)


async def on_message(msg):
    
    global channel
    """
    -Call of looped send
    -Replace invokes, it will automatically replace the emote from the text.
        You can add more 'REPLACES' above.
    """
    if msg.author == bot.user:
        if msg.content.startswith("aarr"):
            channel = msg.channel
            print(str(channel.id))
            try:
                loop = asyncio.get_event_loop()
                #loop.call_later(5, stop)
                task = loop.create_task(periodic())
                loop.run_until_complete(task)
            except asyncio.CancelledError:
                pass

        for k, v in REPLACES.items():
            if k in msg.content:
                await bot.edit_message(msg, msg.content.replace(k, v))
                
    await bot.process_commands(msg)


#==================================
#COMMANDS 


@bot.command(pass_context=True, aliases=['g'])
async def game(ctx, *args):
    """
    Command for changing 'game' status
    """
    if args:
        cstatus = ctx.message.server.get_member(bot.user.id).status
        txt = " ".join(args)
        await bot.change_presence(game=Game(name=txt), status=cstatus)
        msg = await bot.send_message(ctx.message.channel, embed=Embed(color=Color.green(), description="Changed game to `%s`!" % txt))
    else:
        await bot.change_presence(game=None, status=cstatus)
        msg = await bot.send_message(ctx.message.channel, embed=Embed(color=Color.gold(), description="Disabled game display."))
    await bot.delete_message(ctx.message)
    await asyncio.sleep(3)
    await bot.delete_message(msg)


@bot.command(pass_context=True, aliases=['em', 'e'])
async def embed(ctx, *args):
    """
    Sending embeded messages with color
    """
    colors = {
        "red": Color.red(),
        "green": Color.green(),
        "gold": Color.gold(),
        "orange": Color.orange(),
        "blue": Color.blue()
    }
    if args:
        argstr = " ".join(args)
        if "-c " in argstr:
            text = argstr.split("-c ")[0]
            color_str = argstr.split("-c ")[1]
            color = colors[color_str] if color_str in colors else Color.default()
        else:
            text = argstr
            color = Color.default()
        await bot.send_message(ctx.message.channel, embed=Embed(color=color, description=text))
    await bot.delete_message(ctx.message)


@bot.command(pass_context=True)
async def gif(ctx, *args):
    """
    To send gifs by keyword from giphy api
    """
    if args:
        query = " ".join(args)
        index = 0
        if " -" in query:
            try:
                index = int(query.split(" -")[1])
            except:
                pass
            query = query.split(" -")[0]
        giphy = giphypop.Giphy() if GIPHY_TOKEN == "" else giphypop.Giphy(api_key=GIPHY_TOKEN)
        gif = [x for x in giphy.search(query)][index]
        if gif:
            await bot.send_message(ctx.message.channel, gif)
    await bot.delete_message(ctx.message)
        

@bot.command(pass_context=True, aliases=['google'])
async def lmgtfy(ctx, *args):
    """
    Just a simple lmgtfy command, invoche the command and give an arguument, it will search up on google
    """
    if args:
        url = "http://lmgtfy.com/?q=" + "+".join(args)
        await bot.send_message(ctx.message.channel, embed=Embed(description="**[Look here!](%s)**" % url, color=Color.gold()))
    await bot.delete_message(ctx.message)


# Testing if file 'token.txt' exists. Yes LOGIN, No ask for the token, save it and LOGIN
if path.isfile("token.txt"):
    with open("token.txt") as f:
        token = f.readline()
    print("[INFO] Logging in...")
    bot.run(token, bot=False)
else:
    print("Enter your discord account token:")
    token = input()
    print("[INFO] Saving token...")
    with open("token.txt", "w") as f:
        f.write(token)
    print("[INFO] Logging in...")
    bot.run(token, bot=False)

