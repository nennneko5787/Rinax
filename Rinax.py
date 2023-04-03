#Bot Invite URL
#https://discord.com/api/oauth2/authorize?client_id=1092284051794186400&permissions=0&scope=bot
import os
import discord
from urllib.parse import quote
import re
import requests  # 「pip install requests」などが必要
import json
try:
	from discordtoken import token
except ImportError:
	token = os.getenv('DISCORD_TOKEN_RINAX')  #Your TOKEN
from server import keep_alive
intents=discord.Intents.default()
intents.message_content=True

client = discord.Client(intents=intents)  #接続に必要なオブジェクトを生成

@client.event
async def on_ready():
    print("Rinaxの準備が整いました。")
    
@client.event
async def on_message(message):
	if message.author.bot: #BOTの場合は何もせず終了
		return
	print(message.content)
	print(message.content[-2:])
	if message.content[-2:] == "とは":
		async with message.channel.typing():
			marumarumaru_toha = message.content[:-2]
			print("{}をWikipediaで探すのを始めます。。。".format(marumarumaru_toha))
			headers = {'user-agent': 'Rinax Discord Bot/1.0'}
			res = requests.get("https://ja.wikipedia.org/w/api.php?action=query&titles={}&prop=extracts&formatversion=2&format=json&redirects=true".format(quote(marumarumaru_toha)), headers=headers)
			jsondata = json.loads(res.text)
			try:
				print(jsondata['query']['pages'][0]['missing'])
				embed=discord.Embed(title=marumarumaru_toha,description="見つかりませんでした。", color=0x9B95C9, url="https://ja.wikipedia.org/wiki/{}".format(quote("https://ja.wikipedia.org/w/index.php?go=%E8%A1%A8%E7%A4%BA&search={}&title={}&ns0=1".format(jsondata['parse']['title'],quote(jsondata['parse']['title']))))) #埋め込みの説明に、メッセージを挿入し、埋め込みのカラーを紫`#9B95C9`に設定
				embed.set_author(name="Wikipedia")
			except KeyError:
				reg_obj = re.compile(r"<[^>]*?>")
				jsondata['query']['pages'][0]['extract'] = reg_obj.sub("", jsondata['query']['pages'][0]['extract'])
				if len(jsondata['query']['pages'][0]['extract']) > 120:
					description = "{}...".format(jsondata['query']['pages'][0]['extract'][:120])
				else:
					description = jsondata['query']['pages'][0]['extract']
				embed=discord.Embed(title=jsondata['query']['pages'][0]['title'],description=description, color=0x9B95C9, url="https://ja.wikipedia.org/wiki/{}".format(quote(jsondata['query']['pages'][0]['title']))) #埋め込みの説明に、メッセージを挿入し、埋め込みのカラーを紫`#9B95C9`に設定
				embed.set_author(name="Wikipedia")
			await message.channel.send(embed=embed, reference=message)

keep_alive()
client.run(token)