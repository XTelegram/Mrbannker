import logging
import os
import json
from datetime import datetime
import requests
import time
import string
import random
import yaml
import asyncio
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import Throttled
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Configure vars get from env or config.yml
CONFIG = yaml.load(open('config.yml', 'r'), Loader=yaml.SafeLoader)
TOKEN = os.getenv('TOKEN', CONFIG['token'])
BLACKLISTED = os.getenv('BLACKLISTED', CONFIG['blacklisted']).split()
PREFIX = os.getenv('PREFIX', CONFIG['prefix'])
OWNER = int(os.getenv('OWNER', CONFIG['owner']))
ANTISPAM = int(os.getenv('ANTISPAM', CONFIG['antispam']))

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

# Configure logging
logging.basicConfig(level=logging.INFO)

# BOT INFO
loop = asyncio.get_event_loop()

bot_info = loop.run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username
BOT_NAME = bot_info.first_name
BOT_ID = bot_info.id

# USE YOUR ROTATING PROXY API IN DICT FORMAT http://user:pass@providerhost:port

session = requests.Session()

# Random DATA
letters = string.ascii_lowercase
First = ''.join(random.choice(letters) for i in range(6))
Last = ''.join(random.choice(letters) for i in range(6))
PWD = ''.join(random.choice(letters) for i in range(10))
Name = f'{First}+{Last}'
Email = f'{First}.{Last}@gmail.com'
UA = 'Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'


async def is_owner(user_id):
    status = False
    if user_id == OWNER:
        status = True
    return status


@dp.message_handler(commands=['start', 'help'], commands_prefix=PREFIX)
async def helpstr(message: types.Message):
    # await message.answer_chat_action('typing')
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    btns = types.InlineKeyboardButton("Bot Source", url="https://github.com/xbinner18/Mrbannker")
    keyboard_markup.row(btns)
    FIRST = message.from_user.first_name
    MSG = f'''
Hello {FIRST}, Im {BOT_NAME}
U can find my Boss  <a href="tg://user?id={OWNER}">HERE</a>
Cmds /info /gen'''
    await message.answer(MSG, reply_markup=keyboard_markup,
                        disable_web_page_preview=True)


@dp.message_handler(commands=['info', 'id'], commands_prefix=PREFIX)
async def info(message: types.Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        is_bot = message.reply_to_message.from_user.is_bot
        username = message.reply_to_message.from_user.username
        first = message.reply_to_message.from_user.first_name
    else:
        user_id = message.from_user.id
        is_bot = message.from_user.is_bot
        username = message.from_user.username
        first = message.from_user.first_name
    await message.reply(f'''
═════════╕
<b>USER INFO</b>
<b>USER ID:</b> <code>{user_id}</code>
<b>USERNAME:</b> @{username}
<b>FIRSTNAME:</b> {first}
<b>BOT:</b> {is_bot}
<b>BOT-OWNER:</b> {await is_owner(user_id)}
╘═════════''')

@dp.message_handler(commands=['gen'], commands_prefix=PREFIX)
async def binio(message: types.Message):
    await message.answer_chat_action('typing')
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    BIN = message.text[len('/bin '):]

    url = "https://www.deepbrid.com/backend-dl/index.php?page=api&action=generateLink"
    head={'content-type':'application/x-www-form-urlencoded; charset=UTF-8'}
    data = f"link= {BIN}&pass=&boxlinklist=0"
    cookie= {'amember_ru':'rahulnova','amember_rp':'41b8739da7a1766af530a993a4a5c74d50bd1047','cookieconsent_status':'dismiss','crisp-client%2Fsession%2Fffca7959-dfd6-4915-90e2-b2feb57ae28e':'session_f5e79faa-8343-424c-a3cf-7241c05fd264','cf_clearance':'zsY5UafHGge9gvyNDPrjyaGI8oYnuOgf_.uUZ6CrXok-1655790566-0-150;adv1_closed=1','afscr8':'fIGyoi6Zo7pYdDF%2BivnhmPa7wwsNdWl5','PHPSESSID':'20bfbaf6632e67d47af4691b6dccdaf3'}
    resp = requests.post(url, data=data,  headers=head,cookies=cookie)
    y=resp.json()
    olink=y["original_link"]
    fname=y["filename"]
    flink=y["link"]
    fsize=y["size"]
    if y["message"]=='OK':
        olink=y["original_link"]
        fname=y["filename"]
        flink=y["link"]
        fsize=y["size"]
        await message.reply(f'''
                           ✅<b>Link Generated</b>\n'+
                           <b>FileName</b> <code>{fname}</code>\n'+
                           <b>FileSize</b>==> <code>{fsize}</code>\n'+
                           <b>Original Link</b>==> <code>{olink}</code>\n'+
                           <b>New Link</b>==> {flink}\n'+
                           <b>Time-Stamp</b> ==> {datetime.now()}\n'+
                           <b>Plugin-By</b> ~ @Stevenbin''')
    else:
        temp=f'''<code>Link Not Supported</code>'''
        await message.reply(f'{temp}')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop)
