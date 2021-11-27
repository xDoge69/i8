from asyncio.subprocess import STDOUT
import sys
import discord
import os
import random
import datetime
import asyncio
import json
import aiohttp
from discord.ext import commands
import sys
from io import BytesIO, StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
# from PIL import Image

def doge_or_wot(ctx):
  return ctx.author.id == 686220733747298448

def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix,case_insensitive=True, intents=discord.Intents.all())
# client.remove_command('help')

@client.event
async def on_ready():
    guild = client.get_guild(866552630754803732)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"Deez Nuts."))
    print("Bot is Ready.")
    # with open("prefixes.json", "r") as f:
    #     prefixes = json.load(f)
    # prefixes[str(guild.id)] = "%"
    # with open("prefixes.json", "w") as f:
    #     json.dump(prefixes, f)

# WELCOME
@client.event
async def on_member_join(member):
  welcch = client.get_channel(892770226259755048)
  await welcch.send(member.mention)
  embed = discord.Embed(
  description=f"""
Welcome to **Doge's Server!**

-Check these out:
> ❤️<#866552774630965258>
> ❤️<#892796760156684348>
-Hope you have a Nice Stay!
  """,
  color = discord.Colour.dark_blue())
  embed.set_author(name=member.name, icon_url=member.avatar.url)
  embed.set_footer(text=f"You're Member {member.guild.member_count}!")
  embed.set_thumbnail(url=member.avatar.url)
  await welcch.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
  raise error

@client.command(aliases=['playing'])
@commands.has_permissions(administrator=True)
async def p(ctx, *, status):
  await client.change_presence(activity=discord.Game(name=status))
  await ctx.send("✅ Successful.")

@client.command(aliases=['watching'])
@commands.has_permissions(administrator=True)
async def w(ctx, *, status):
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
  await ctx.send("✅ Successful.")

@client.command(aliases=['listening'])
@commands.has_permissions(administrator=True)
async def l(ctx, *, status):
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
  await ctx.send("✅ Successful.")

@client.command(aliases=['compete', 'competing'])
async def c(ctx, *, status):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status))
    await ctx.send("✅ Successful.")
 
@client.command()
async def disc(ctx):
    await ctx.send("https://discord.gg/rjGWmGwAtU")

deleted = set()
@client.event
async def on_message_delete(message):
  if message.mentions:
    for s in message.mentions:
      if s == message.author:
        return
      elif s == client.user:
        return
      elif message.author == client.user:
        return
      elif message.author.bot == True:
        return
      elif s.bot == True:
        return
      else:
        await message.channel.send(f"{s.mention} was Ghost Pinged by {message.author.mention}.")
  msg = message.content or message.attachments
  if not message.author.bot == True:
    if not msg == message.attachments:
      deleted.clear()
      deleted.add(message)

@client.command(description=f"snipe", aliases=['snip'])
async def snipe(ctx):
  if deleted == set():
    await ctx.send("There's nothing to snipe!")
    return
  else:
    for msg in deleted:
      if msg.channel.id == ctx.message.channel.id:
        embed = discord.Embed(timestamp = msg.created_at,
        description = msg.content,
        color = discord.Colour.dark_green())
        embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
        await ctx.send(embed=embed)
      else:
        await ctx.send("There's nothing to snipe!")

@client.command(description=f"cprefix <prefix>")
@commands.has_permissions(administrator=True)
async def cprefix(ctx, *, prefix):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)
  prefixes[f'{ctx.guild.id}'] = f"{prefix}"
  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f)
  await ctx.send(f"The prefix was changed to **{prefix}**")

@client.command(description=f"purge <amount>")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=0):
    await ctx.message.delete()
    channel = ctx.message.channel
    await channel.purge(limit=amount)

@purge.error
async def purgerror(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You're missing the **Manage Messages** Permission.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify an Amount.")

# KICK
@client.command(description="kick <member> [reason]")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.send(reason)
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked!')

@kick.error
async def kickrror(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are Missing the **Kick Members** Permission.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify the Member you want to Kick.")

# BAN AND UNBAN
@client.command(description=f"ban <member> [reason]")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user:discord.User, *, arg=None):
  if arg == None:
    arg = 'No Reason given.'
  try:
    await ctx.guild.ban(user, reason=arg)
    embed = discord.Embed(description=f"""
✅ ***{user} was Banned.*** | {arg}
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)
  except:
    await ctx.send("I could not ban that user.")

@ban.error
async def banerror(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are Missing the **Ban Members** Permission.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'''
**Ban**

**How To Use:**
{get_prefix(client, ctx.message)}ban <user> <reason>

**Example Use:**
{get_prefix(client, ctx.message)}ban @-1Doge#9999 Being Unfriendly
        ''')

@client.command(description=f"unban <member>")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
  try:
    await ctx.guild.unban(user)
    embed = discord.Embed(description=f"✅ ***{user} was unbanned.***", color = discord.Colour.green())
    await ctx.send(embed=embed)
  except:
    await ctx.send("Not a previously banned member.")

@unban.error
async def unbanerror(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are Missing the **Ban Members** Permission.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"""
**Unban**

**How To Use:**
{get_prefix(client, ctx.message)}unban <user>

**Example Use:**
{get_prefix(client, ctx.message)}unban @-1Doge#4337
        """)

@client.command()
@commands.has_permissions(manage_messages=True)
async def say (ctx, *, arg):
  await ctx.message.delete()
  await ctx.send(arg)

@say.error
async def sayrror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You can't use that.")


@client.command(description=f"mute <member> [time] [reason]")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member:discord.Member, dtime=None,*, reason=None):
  if dtime is None:
    dtime = 300
  mute_role = ctx.guild.get_role(867724234728669214)
  if (member.guild_permissions.administrator):
    return await ctx.send(f"{member} is an Admin so I cannot mute them.")
  else:
    if discord.utils.get(member.roles, name='Muted') is not None:
      await ctx.send(F"{member} is already Muted.")
    else:
      await member.add_roles(mute_role)
      embed = discord.Embed(
      description=f"***✅ {member} was Muted | Reason: {reason}***",
      color = discord.Colour.dark_green())
      await ctx.send(embed=embed)
      def convert(dtime):

        pos = ['s', 'm', 'h', 'd']
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
        unit = dtime[-1]
        if unit not in pos:
          return -1
        try:
          val = int(dtime[:-1])
        except:
          return -2
        return val * time_dict[unit]
      converted_time = convert(dtime)
      await asyncio.sleep(converted_time)
      await member.remove_roles(mute_role)
      embed = discord.Embed(description=f"✅ ***{member} was Unmuted.***", color = discord.Colour.green())
      await ctx.send(embed=embed)

@mute.error
async def murror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You are Missing the **Manage Roles** Permission.")
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'''
**Mute**

**How To Use:**
{get_prefix(client, ctx.message)}mute <member> <reason>

**Example Use:**
{get_prefix(client, ctx.message)}mute @-1Doge#4337 Breaking The Rules.
    ''')

@client.command(description=f"unmute <member>")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx,member : discord.Member):
  muterole = ctx.guild.get_role(867724234728669214)
  if discord.utils.get(member.roles, name='Muted') is None:
    return await ctx.send("That Member is not Muted.")
  else:
    await member.remove_roles(muterole)
    embed = discord.Embed(description=f"✅ ***{member} was unmuted.***",
      color = discord.Colour.green())
    await ctx.send(embed=embed)

@unmute.error
async def unmurror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You don't have the perms to use this command.")

@client.command(description=f"crole <rolename>",aliases=['createrole', 'creater'])
@commands.has_permissions(manage_roles=True) 
async def crole(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'✅ Role `{name}` has been Created.')

@crole.error
async def crolerror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You are Missing the **Manage Roles** Permission.")

@client.command(description="drole <role>")
@commands.has_permissions(manage_roles=True)
async def drole(ctx, *, role: discord.Role):
    await role.delete()
    await ctx.send(f'✅ Role `{role}` has been Deleted')

@drole.error
async def drror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You are Missing the **Manage Roles** Permission.")

@client.command()
@commands.check(doge_or_wot)
async def disable(ctx, *, command: client.get_command):
  if not command.enabled:
    await ctx.send(f"❌ **{command}** is already Disabled.")
  else:
    command.enabled = False
    await ctx.send(f"✅ **{command} has Been Disabled.")

@client.command()
@commands.check(doge_or_wot)
async def enable(ctx, *, command: client.get_command):
  if command.enabled:
    await ctx.send(f"❌ **{command}** is Already Enabled.")
  else:
    command.enabled = True
    await ctx.send(f"✅ **{command}** has been Enabled.")

#ROLES ADDING AND REMOVING
@client.command(description=f"role <member> [roles...]")
@commands.has_permissions(manage_roles=True)
async def role(ctx,member: discord.Member,*,input_role):
    input_role = input_role.split(', ')
    server_roles = ctx.guild.roles
    for r in input_role:
        for s in server_roles:
            if s.name.lower().startswith(r.lower()):
                if s not in member.roles:
                    await member.add_roles(s)
                    embed = discord.Embed(description=f"✅ **Added {s.mention} to {member.mention}**")
                    await ctx.send(embed=embed)
                else:
                  await member.remove_roles(s)
                  embed = discord.Embed(description=f"✅ **Removed {s.mention} from {member.mention}**")
                  await ctx.send(embed=embed)

@role.error
async def rolerror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("❌ You are Missing the **Manage Role** Permission.")
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"""
**Role**

**How To Use:**
{get_prefix(client, ctx.message)}role <member> <roles>

**Example Use:**
{get_prefix(client, ctx.message)}role @-1Doge#4337 Community
  """)

@client.command(description=f"slowmode <seconds>")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
  await ctx.channel.edit(slowmode_delay=seconds)
  await ctx.send(f"✅ Set Slowmode To {seconds}!")

@slowmode.error
async def slowmodor(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You are Missing the **Manage Channels** Permission.")

@client.command(description=f"sinfo", aliases=['serverinfo'])
async def sinfo(ctx):
  name = ctx.guild.name
  id = ctx.guild.id
  owner = ctx.guild.owner
  membercount = ctx.guild.member_count
  channels = ctx.guild.text_channels
  voicech = ctx.guild.voice_channels
  roles = ctx.guild.roles
  categories = ctx.guild.categories
  embed = discord.Embed(
    title=name,
    color = discord.Colour.dark_blue()
  )
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Member Count", value=membercount, inline=True)
  embed.add_field(name="Role Count", value=f"{len(roles)}")
  embed.add_field(name="Channel Categoies", value=f"{len(categories)}", inline=True)
  embed.add_field(name="Text Channels", value=f"{len(channels)}", inline=True)
  embed.add_field(name="Voice Channels", value=f"{len(voicech)}", inline=True)
  embed.set_thumbnail(url=ctx.guild.icon_url)
  embed.set_footer(text=f"ID: {id}")
  await ctx.send(embed=embed)

@client.command(dewscription=f"emojiadd <emojilink> <emojiname>", aliases=['eadd', 'emadd', 'steal'])
@commands.has_permissions(manage_emojis=True)
async def emojiadd(ctx, url: str=None, *, name):
  guild = ctx.guild
  async with aiohttp.ClientSession() as ses:
    async with ses.get(url) as r:
      try:
        img_or_gif = BytesIO(await r.read())
        b_value = img_or_gif.getvalue()
        if r.status in range(200, 299):
          emoji = await guild.create_custom_emoji(image=b_value, name=name)
          ternary = f'<a:{name}:{emoji.id}>' if emoji.animated==True else f'<:{name}:{emoji.id}>'
          em = discord.Embed(description=f"✅ Successfully created Emoji {ternary}", color = discord.Colour.green())
          await ctx.send(embed=em)
          await ses.close()
        else:
          em = discord.Embed(description=f"❌ Error when making request | {r.status} response.", color = discord.Colour.red())
          await ctx.send(embed=em)
          await ses.close()
      except discord.HTTPException:
        em = discord.Embed(description=f"❌ File Size is Too Big or Max Emoji Limit Reached.")
        await ctx.send(embed=em)

@emojiadd.error
async def emojiaddrror(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are Missing the **Manage Server** Permission.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"""
**Steal**

**How To Use:**
{get_prefix(client, ctx.message)}steal <emojilink> <emojiname>

**Example Use:**
{get_prefix(client, ctx.message)}steal <https://cdn.discordapp.com/emojis/89301115824.png?size=128> thonk
        """)

@client.command(description=f"emojiremove <emoji>", aliases=['eremove', 'emremove'])
@commands.has_permissions(manage_emojis=True)
async def emojiremove(ctx, emoji: discord.Emoji):
  em = discord.Embed(description=f"✅ Successfully deleted Emoji {emoji}")
  await ctx.send(embed=em)
  await emoji.delete()

@emojiremove.error
async def emojierror(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are Missing the **Manage Server** Permission.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"""
**Emremove**

**How To Use:**
{get_prefix(client, ctx.message)}emremove <emoji>

**Example Use:**
{get_prefix(client, ctx.message)}emremove :skull:
        """)

@client.command(description=f"membercount")
async def membercount(ctx):
  guild = ctx.guild
  embed=discord.Embed(title="Members", description=guild.member_count, color = discord.Colour.dark_blue())
  await ctx.send(embed=embed)

@client.command(description=f"av [member]", aliases=['avatar'])
async def av(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author
  embed = discord.Embed(
    title = f"{member}'s Avatar!",
    color = discord.Colour.dark_blue()
  )
  embed.set_author(name=f"{member}", icon_url=f"{member.avatar.url}")
  embed.set_image(url=member.avatar.url)

  await ctx.send(embed=embed)

@client.command(description=f"lock [channel]")
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel=None):
  roleneedstobelocked = ctx.guild.get_role(866553229591445504)
  if channel == None:
    channel = ctx.channel
    await channel.set_permissions(roleneedstobelocked, send_messages=False)
    embed = discord.Embed(title="Channel Locked.", description=f"""
*✅ **{ctx.channel.mention} Has Been Locked!***
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)
  else:
    await channel.set_permissions(roleneedstobelocked, send_messages=False)
    embed = discord.Embed(title="Channel Locked.", description=f"""
*✅ **{channel.mention} Has Been Locked!***
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)

@client.command(description=f"unlock [channel]")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel=None):
  roleneedstobeunlocked = ctx.guild.get_role(866553229591445504)
  if channel == None:
    channel = ctx.channel
    await channel.set_permissions(roleneedstobeunlocked, send_messages=None)
    embed = discord.Embed(title="Channel Unlocked.", description=f"""
*✅ **{ctx.channel.mention} Has Been Unlocked!***
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)
  else:
    await channel.set_permissions(roleneedstobeunlocked, send_messages=None)
    embed = discord.Embed(title="Channel Unlocked.", description=f"""
*✅ **{channel.mention} Has Been Unlocked!***
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)

@client.command(description=f"sname <name>")
@commands.has_any_role(866553374149443585)
async def sname(ctx, *, gname):
  guild = ctx.guild
  embed = discord.Embed(description=f"✅ Server Name Changed from **{guild.name}** to **{gname}**.", color = discord.Colour.green())
  await ctx.send(embed=embed)
  await guild.edit(name=gname)

@client.command(description=f"nick <member> <nickname>", aliases=['nickname', 'setnick'])
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member=None, *, nickname):
  if member == None:
    member = ctx.message.author
  try:
    await member.edit(nick=nickname)
    embed = discord.Embed(description=f"✅ Nickname changed to {nickname}", color = discord.Colour.green())
    await ctx.send(embed=embed)
  except:
    return await ctx.send(f"I could not change the name for {member}.")

@nick.error
async def nickerror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You are Missing the **Manage Nicknames** Permission.")

@client.command(description=f"remind <time> <task>",aliases=['remindme', 'rem'])
async def remind(ctx, time, *, task):
  def convert(time):
    pos = ['s', 'm', 'h', 'd']
    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
    unit = time[-1]
    if unit not in pos:
      return -1
    try:
      val = int(time[:-1])
    except:
      return -2
    return val * time_dict[unit]
  converted_time = convert(time)
  if converted_time == -1:
    await ctx.send("You didn't answer the time correctly.")
    return
  if converted_time == -2:
    await ctx.send("The Time must be an integer.")
    return
  await ctx.send(f"Reminder set for **{task}**, it will last **{time}**.")
  await asyncio.sleep(converted_time)
  embed = discord.Embed(title="Reminder!", description=f"""
Hey {ctx.author.mention} here's your reminder for **{task}**! [Jump To Original Message]({ctx.message.jump_url})
  """, color = discord.Colour.green(), timestamp = datetime.datetime.now(datetime.timezone.utc))
  await ctx.author.send(embed=embed)
  await ctx.send(f"Check your DMs {ctx.author.mention}")

class Help(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
    self.value = None

  @discord.ui.button(label='Moderation', style=discord.ButtonStyle.green)
  async def mod(self, button: discord.ui.Button, interaction: discord.Interaction):
    embed = discord.Embed(title="Moderation\nOnly Moderators and above can use these Commands.", color = discord.Colour.blue())
    embed.add_field(name="Purge", value=f"Purges Messages.\nUsage:\n**{get_prefix(client, interaction.message)}purge <amount>**", inline=True)
    embed.add_field(name="Kick", value=f"Kicks a User.\nUsage:\n**{get_prefix(client, interaction.message)}kick <user> [reason]**", inline=True)
    embed.add_field(name="Ban", value=f"Bans a User.\nUsage:\n**{get_prefix(client, interaction.message)}ban <user> [reason]**", inline=True)
    embed.add_field(name="Unban", value=f"Unbans a User.\nUsage:\n**{get_prefix(client, interaction.message)}unban <user>**", inline=True)
    embed.add_field(name="Mute", value=f"Mutes a User.\nUsage:\n**{get_prefix(client, interaction.message)}mute <user> [reason]**", inline=True)
    embed.add_field(name="Unmute", value=f"Unmutes a User.\nUsage:\n**{get_prefix(client, interaction.message)}unmute <user>**", inline=True)
    embed.add_field(name="Lock", value=f"Locks The Channel.\nUsage:\n**{get_prefix(client, interaction.message)}lock [channel]**", inline=True)
    embed.add_field(name="Unlock", value=f"Unlocks A Previously Locked Channel.\nUsage:\n**{get_prefix(client, interaction.message)}unlock [channel]**", inline=True)
    embed.add_field(name="Setnick", value=f"Sets the Nickname of a Member.\nUsage:\n**{get_prefix(client, interaction.message)}setnick <member> <nickname>**", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    self.value = True

  @discord.ui.button(label='Roles', style=discord.ButtonStyle.grey)
  async def romle(self, button: discord.ui.Button, interaction: discord.Interaction):
    embed = discord.Embed(title="Roles\nOnly Moderators and above can use these Commands.", color = discord.Colour.blue())
    embed.add_field(name="Role", value=f"Adds a role to a member. \nUsage:\n**{get_prefix(client, interaction.message)}role <member> [roles...]**", inline=True)
    embed.add_field(name="Crole", value=f"Creates a Role. \nUsage:\n**{get_prefix(client, interaction.message)}crole <role>**", inline=True)
    embed.add_field(name="Drole", value=f"Deletes a Role. \nUsage:\n**{get_prefix(client, interaction.message)}drole <role>**", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    self.value = False
  
  @discord.ui.button(label='Emojis', style=discord.ButtonStyle.grey)
  async def emojis(self, button: discord.ui.Button, interaction: discord.Interaction):
    embed = discord.Embed(title="Emojis\nOnly Moderators with the **Manage Emojis** Permission Can Use These Commands.", color = discord.Colour.blue())
    embed.add_field(name="Emojiadd", value=f"Adds An Emoji To The Server, Make Sure The Max Emoji Limit isn't full!\nUsage:\n**{get_prefix(client, interaction.message)}emojiadd <emojilink> <emojiname>**", inline=True)
    embed.add_field(name='Emojiremove', value=f'Removes an Emoji From The Server.\nUsage:\n**{get_prefix(client, interaction.message)}emojiremove <emoji>**', inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    self.value = False
  
  @discord.ui.button(label='Others', style=discord.ButtonStyle.grey)
  async def others(self, button: discord.ui.Button, interaction: discord.Interaction):
    embed = discord.Embed(title="Others\nOnly Some commands can be used by everyone.", color = discord.Colour.blue())
    # embed.add_field(name="Toggle", value=f"Enable and Disable Commands. \nUsage:\n**{get_prefix(client, ctx.message)}toggle <command>**", inline=True)
    embed.add_field(name="Avatar", value=f"Displays the Avatar of a user. \nUsage:\n**{get_prefix(client, interaction.message)}av [user]**", inline=True)
    embed.add_field(name="Slowmode", value=f"Sets the slowmode in a channel. \nUsage:\n**{get_prefix(client, interaction.message)}slowmode <seconds>**", inline=True)
    embed.add_field(name="Snipe", value=f"Snipes the Last Deleted Message!\nUsage:\n{get_prefix(client, interaction.message)}snipe", inline=True)
    embed.add_field(name="Disc", value=f"Gives The Permanent Link For The Server.\nUsage:\n**{get_prefix(client, interaction.message)}disc**", inline=True)
    embed.add_field(name="Say", value=f"The Bot Says The Message.\nUsage:\n**{get_prefix(client, interaction.message)}say <message>**", inline=True)
    embed.add_field(name="Membercount", value=f"The Member Count.\nUsage:\n**{get_prefix(client, interaction.message)}membercount**", inline=True)
    embed.add_field(name="Serverinfo", value=f"Gives info about the Server.\nUsage:\n**{get_prefix(client, interaction.message)}sinfo**", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    self.value = False
  
@client.command(description=f"run <code>")
async def run(ctx, *, code):
  if ctx.author.id == 686220733747298448:
    if not code.startswith('```py'):
      return await ctx.send("Your message should start with \```py and end with \```")
    if not code.endswith('```'):
      return await ctx.send("Your message should start with \```py and end with \```")
    code = code[+5:]
    code = code[:-3]
    with stdoutIO() as s:
      exec(code)
    output = s.getvalue()
    await ctx.send(f"** **{output}")
  else:
    await ctx.send("I totally don't have a command like that 😶")

@client.command(description=f"simprate [member]")
async def simprate(ctx, *, member: discord.Member=None):
    rates = random.randint(1, 100)
    if member == None:
      member = ctx.author
    embed = discord.Embed(description=f"{rates}%", color = discord.Colour.blurple())
    embed.set_author(name=f"{member} is a Simp by:", icon_url=member.avatar.url)
    await ctx.send(embed=embed)

@client.command(description="remove")
async def remove(ctx, *, command):
  if ctx.author.id == 686220733747298448:
    client.remove_command(command)
    await ctx.send(f"Removed {command}")

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
      view = Help()
      embed=discord.Embed(title="Help Manual", description=f"""
Hello! Here's my help manual, first there are a few things you must know before using the commands;

Arguments - Arguments are the words that you pass in whenever you use a command like: \**{self.context.prefix}ban -1Doge#4337 spamming** <- Here, **ban** is the command and **-1Doge#4337** and **spamming** are the arguments.
An argument can be optional or required.

<argument>
> This means the argument is __**required**__.
[argument]
> This means the argument is **__optional__**.
[A|B]
> This means that it can be either **A** or **B**.
[argument...]
> This means you can have **__multiple__** arguments.

it should also be noted that **__You do not have to type in the brackets.__**

You can click the buttons below to know more about each category.
Type **{self.context.prefix}help <command>** to know how you should use a command.
    """, color=discord.Colour.blue())
      await self.context.send(embed=embed,view=view)
      await view.wait()
       
    async def send_command_help(self, command: client.get_command):
      if command.description == '':
        await self.context.send("No description provided.")
      else:
        await self.context.send(f'**{self.context.prefix}{command.description}**')
      
    async def send_group_help(self, group):
        await self.context.send("This is help group")
    
    async def send_cog_help(self, cog):
        await self.context.send("This is help cog")

client.help_command = MyHelp()

@client.command(description="dcat <category> (Can ONLY Be Used By Doge.)")
@commands.check(doge_or_wot)
async def dcat(ctx, *, c: discord.CategoryChannel):
  await ctx.message.delete()
  for s in c.channels:
    await s.delete()
  await c.delete()
  await ctx.send("✅ Success.", delete_after=4)

client.run()
