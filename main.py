import os
import discord
from discord.ext import commands,tasks
import aiohttp
import json
import random
from colorama import Fore, Style
import httpx
import asyncio
import threading
from flask import Flask
import pyfiglet
import time
import websocket
os.system("clear||cls")

# --- DISCORD.PY-SELF FIX START ---
from discord.gateway import DiscordWebSocket

async def patched_identify(self):
    payload = {
        'op': self.IDENTIFY,
        'd': {
            'token': self.token,
            'properties': {
                '$os': 'Windows',
                '$browser': 'Chrome',
                '$device': '',
                '$referrer': '',
                '$referring_domain': '',
            },
            'compress': self._compress,
            'large_threshold': 250,
        }
    }
    if hasattr(self, '_ext_modifiers') and self._ext_modifiers:
        payload['d'].update(self._ext_modifiers)
    if self._sequence:
        payload['d']['sequence'] = self._sequence

    await self.send_json(payload)

DiscordWebSocket.identify = patched_identify
# --- DISCORD.PY-SELF FIX END ---


with open("config.json", "r", encoding="utf-8") as f:
    cf = json.load(f)

mobile_status = cf["Mobile_Status"]
status_texts = cf["Status_Texts"]
status_emojis = cf["Status_Emojis"]
webhook = cf["Webhook"]
invg = cf["Invite_Guild_ID"]
stype = cf["Status"]
delay = cf["Delay"]
guild_id_ = cf["Guild_ID"]
channels = cf["J4J_Channel_Names"]
cmsgs = cf["Channel_Messages"]
dmsgs = cf["DM_Messages"]
dnmsgs = cf["Done_Messages"]
wb_ = cf["WebServer"]
webhook = webhook.replace("https://discord.com", "https://canary.discord.com")

def send_request(token: str):
    webher = websocket.WebSocket()
    webher.connect(url= 'wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream')
    while True:
      webher.send(json.dumps({"op":2,"d":{"token": token,"capabilities":125,"properties":{"os":"Discord iOS","browser":"Discord iOS","device":"iOS","system_locale":"fr","browser_user_agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0","browser_version":"95.0","os_version":"","referrer":"https://discord.com/","referring_domain":"discord.com","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":107767,"client_event_source":None},"presence":{"afk":False},"compress":False,"client_state":{"guild_hashes":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1}}}))
      time.sleep(5)

class logger:
  def log(content):
    try:
      httpx.post(webhook, json={'content': content})
    except Exception as e:
      print(e)
      colors.warning("Failed To Send Log")

class colors:
  def ask(qus):
    print(f"{Fore.LIGHTMAGENTA_EX}[?]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

  def what(txt):
    print(f"{Fore.LIGHTBLUE_EX}[?]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def banner(txt):
    print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{txt}{Fore.RESET}{Style.NORMAL}")

  def error(txt):
    print(f"{Fore.RED}[{random.choice(['-', '!'])}]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

  def sucess(txt):
    print(f"{Fore.GREEN}[+]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def warning(txt):
    print(f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

  def log(txt):
    print(f"{Fore.LIGHTMAGENTA_EX}[!]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def msg(txt, idx):
    return f"{Fore.LIGHTBLUE_EX}[{idx+1}]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}"
    
  def ask2(qus):
    print(f"{Fore.LIGHTMAGENTA_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

  def ask3(qus):
    print(f"{Fore.LIGHTBlUE_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

async def identify(self) -> None:
        """Sends the IDENTIFY packet."""
        prop = self._super_properties
        prop["os"] = "Windows"
        prop["browser"] = "Discord"
        prop["device"] = "Desktop"
        prop["$os"] = "Windows"
        prop["$browser"] = "Discord"
        prop["$device"] = "Desktop"
        
        payload = {
            'op': self.IDENTIFY,
            'd': {
                'token': self.token,
                'capabilities': 509,
                'properties': prop,
                'presence': {
                    'status': 'online',
                    'since': 0,
                    'activities': [],
                    'afk': False,
                },
                'compress': False,
                'client_state': {
                    'guild_hashes': {},
                    'highest_last_message_id': '0',
                    'read_state_version': 0,
                    'user_guild_settings_version': -1,
                },
            },
        }

        if not self._zlib_enabled:
            payload['d']['compress'] = True

        await self.call_hooks('before_identify', initial=self._initial_identify)
        await self.send_as_json(payload)

async def start(self, token: str, *, reconnect: bool = True) -> None:
        """|coro|
        A shorthand coroutine for :meth:`login` + :meth:`connect`.
        """
        # User token için özel temizleme
        token = token.strip().strip('"').strip("'").strip()
        
        # Token'ın başında "Bot " varsa kaldır (user token için gerekli değil)
        if token.startswith("Bot "):
            token = token[4:]
            
        colors.warning(f"Logging In As -> {token[:12]}*****!")
        try:
            # User token için login (bot parametresi olmadan)
            await self.login(token)
            await self.connect(reconnect=reconnect)
        except Exception as e:
            print(f"[!] Login Hatası: {e}")
            if "improper" in str(e).lower() or "unauthorized" in str(e).lower():
                colors.error(f"Invalid User Token -> {token[:12]}*****!")
                colors.warning("User token'ını yeniden alın. F12 -> Network -> XHR -> Authorization header'dan alabilirsiniz.")
            elif "forbidden" in str(e).lower():
                colors.error(f"User Account Disabled/Suspended -> {token[:12]}*****!")
            else:
                colors.warning("Başka bir hata oluştu. (Rate Limit, Timeout, Bağlantı sorunu vs.)")

discord.Client.start = start
commands.Bot.start = start

if mobile_status:
  discord.gateway.DiscordWebSocket.identify = identify

def reset_db():
  with open("database.json", "r") as f:
    file = json.load(f)
  file["ignore"] = []
  with open("database.json", "w") as f:
    json.dump(file, f, indent=4)

def set_db(id,bid):
  with open("database.json", "r") as f:
    file = json.load(f)
  file["ignore"].append(f"{id}:{bid}")
  with open("database.json", "w") as f:
    json.dump(file, f, indent=4)

def has_ignore(id,bid):
  with open("database.json", "r") as f:
    file = json.load(f)
    ids = file["ignore"]
  toreturn = True if f"{id}:{bid}" in ids else False
  return toreturn

DB_RESET = False

class BotCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.prop = None

  @tasks.loop(seconds=15)
  async def activity_task(self):
    emo = random.choice(status_emojis)
    text = random.choice(status_texts)
    if stype == "online":
      stf = discord.Status.online
    elif stype == "idle":
      stf = discord.Status.idle
    elif stype == "dnd":
      stf = discord.Status.dnd
    await self.bot.change_presence(activity=discord.CustomActivity(name=text, emoji=emo), status=stf)

  @tasks.loop(seconds=delay)
  async def channel_task(self):
    guild = self.bot.get_guild(guild_id_)
    try:
      for channel in guild.channels:
        for cnl in channels:
          if cnl in channel.name:
            if self.bot:
              msg = random.choice(cmsgs)
              async with channel.typing():
                await asyncio.sleep(9)
                await channel.send(msg)
                logger.log(f"Successfully Sent -> {msg} In {channel.name} From {self.bot.user}")
                colors.sucess(f"Successfully Sent -> {msg} In {channel.name} From {self.bot.user}")
    except Exception as e:
      colors.error(f"error -> {e}")
      logger.log(f"error -> {e}, @")
        
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return
    if message.guild:
      return
    if message.author.id == self.bot.user.id:
      return
    try:
      snap = has_ignore(message.author.id, self.bot.user.id)
      if snap:
        return
      set_db(message.author.id, self.bot.user.id)
      async with message.channel.typing():
        await asyncio.sleep(7)
        msg = random.choice(dmsgs)
        await message.channel.send(msg)
        async with message.channel.typing():
          await asyncio.sleep(14)
          await message.channel.send(random.choice(dnmsgs))
        colors.sucess(f"Received DM, Sent Done, Start DM Message To {message.author} From {self.bot.user}")
    except Exception as e:
      colors.error(f"error -> {e}")
      logger.log(f"error -> {e}, @everyone")
  
  @commands.Cog.listener()
  async def on_member_join(self, member):
    id = member.guild.id
    if id != invg:
      return
    colors.sucess(f"{member} Just Joined Our Server!")
    logger.log(f"{member} Just Joined Our Server!")
    
  @commands.Cog.listener("on_connect")
  async def on_connect_two(self):
    await self.channel_task.start()
    
  @commands.Cog.listener()
  async def on_disconnect(self):
    colors.warning("Disconnected From Discord., Changing IP.")
    logger.log("Disconnected from Discord, Changing IP.")
    os.system("kill 1")
  @commands.Cog.listener()
  async def on_ready(self):
    global DB_RESET
    try:
        prop = self.bot.http.super_properties
        self.prop = prop
        if hasattr(self.bot, 'ws') and self.bot.ws:
            self.bot.ws._super_properties = prop
        prop["os"] = "Discord iOS"
        prop["browser"] = "Discord iOS"
        prop["device"] = "iOS"
        prop["$os"] = "Discord iOS"
        prop["$browser"] = "Discord iOS"
        prop["$device"] = "iOS"
    except Exception as e:
        colors.warning(f"Could not set properties: {e}")
    
    colors.sucess(f"Connected To {self.bot.user}!")
    logger.log(f"Connected To {self.bot.user}!")
    
    # Start tasks
    try:
        if not self.activity_task.is_running():
            self.activity_task.start()
        colors.sucess(f"Tasks Were Started For {self.bot.user}")
    except Exception as e:
        colors.warning(f"Could not start activity task: {e}")
    
    if DB_RESET:
      return
    DB_RESET = True
    reset_db()

# --- YENİ TOKEN SİSTEMİ (RENDER UYUMLU) ---
import os
env_token = os.getenv("DISCORD_TOKEN")

tokens = []
if env_token:
    # Virgülle ayrılmış tokenları listeye çevirir
    tokens = [t.strip().strip('"').strip("'") for t in env_token.split(",") if len(t.strip()) > 50]

if not tokens:
    print("UYARI: DISCORD_TOKEN bulunamadı! Render Environment Variables kısmını kontrol edin.")
# ------------------------------------------


app = Flask(__name__)

@app.route("/")
def index():
  return "J4J Bot, 24/7 Web Server"

def run_app():
  app.run(port=8080, host="0.0.0.0")

if wb_:
  threading.Thread(target=run_app).start()
  time.sleep(2)

bnr = pyfiglet.figlet_format("J4J BOT")
colors.banner(bnr+"\n")
colors.warning("© Developed By Alien")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def run_bots():
    tasks = []
    for token in tokens:
        client = commands.Bot(
            command_prefix="^", 
            help_command=None, 
            self_bot=True
        )
        await client.add_cog(BotCog(client))
        task = asyncio.create_task(client.start(token, reconnect=True))
        tasks.append(task)
        await asyncio.sleep(1)  # Delay between bot starts
    
    await asyncio.gather(*tasks, return_exceptions=True)

try:
    loop.run_until_complete(run_bots())
except KeyboardInterrupt:
    colors.warning("Bot stopped by user")
except Exception as e:
    colors.error(f"Error running bots: {e}")
finally:
    loop.close()
