#ponkbot by ilerm
from mcstatus import MinecraftServer
import time

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import requests
import json

##### Global Variables #####
sSurv = MinecraftServer.lookup("server ip") #REDACTED
sCrea = MinecraftServer.lookup("server ip") #REDACTED
freeForAll = False
pinataTime = False
pinataHealth = 0
fallenMoney = 0
gatherLeft = 0
canGather = [0,0,0]
smacked = [0,0,0]
confirmAsked = False

bot = commands.Bot(command_prefix='.')

StrList = "/home/ubuntu/pokedex/list.txt"
StrBank = "/home/ubuntu/pokedex/bank.txt"
StrNotes = "/home/ubuntu/pokedex/notes.txt"
StrEmoji = "/home/ubuntu/pokedex/emoji.txt"

##### API KEYS #####
dic_app_id = 'dictionary app id goes here'   #REDACTED
dic_app_key = 'dictionary app key goes here' #REDACTED

##### Pokemon list #####
fpd = open (StrList , "r", encoding="utf-8")
myDex = [[num for num in line.split(',')] for line in fpd]
fpd.close()

##### Emoji list #####
femo = open (StrEmoji , "r", encoding="utf-8")
emojis = femo.readlines()
femo.close()

##### Global Arrays #####
gottemArr = ["https://i.imgur.com/Tn7bTTz.jpg",
"https://pbs.twimg.com/media/CPgytitWsAA8gNd.jpg",
"beep beep bip  beep beep beep  beep  beep  bip  beep beep"]

yeArr = ["https://giphy.com/gifs/jack-nicholson-nodding-anger-management-S3Ot3hZ5bcy8o",
"http://i43.tinypic.com/ac8ye8.gif",
"https://media.tenor.com/images/782c3bc5d8e758e78f61d86166744bdb/tenor.gif",
"https://media.giphy.com/media/i79P9wUfnmPyo/giphy.gif",
"https://media.giphy.com/media/XenWVVdSzaxLW/giphy.gif"]

dooArr = ["https://img.4plebs.org/boards/pol/image/1495/67/1495675425533.gif",
"https://78.media.tumblr.com/68deb8b188a8f6262e2b2f4d21f5c41d/tumblr_mw3f9neC6C1s4db95o1_500.gif"]

noballsArr = ["https://imgur.com/SZLp1kk",
"https://i.imgur.com/8lBqQnW.gifv"]

nugArr = ["https://cdn.discordapp.com/attachments/154608293338284032/517664261355470858/unknown.png",
"https://i.imgur.com/dO6APX2.png"]


@bot.command(pass_context=True)
async def define(ctx, word):
	url = 'https://od-api.oxforddictionaries.com/api/v1/entries/en/' + word.lower()
	r = requests.get(url, headers = {'app_id': dic_app_id, 'app_key': dic_app_key})

	msg = '**'+word+':**\n'
	data = r.json()
	if data.get('results'):
		data = data.get('results')[0]
		lex = data.get('lexicalEntries')
		if lex:
			lex = lex[0]
			ent = lex.get('entries')[0]
			senses = ent.get('senses')
			if senses:
				definitions = senses[0].get('definitions')
				if definitions:
					msg += definitions[0]
	await bot.say(msg)


@bot.command(pass_context=True)
async def emoji(ctx, num=1):
	if num > 10:
		num = 10

	if num < 1:
		num = 1

	text = ""
	for x in range(num):
		i = random.randint(0,len(emojis)-1)
		text += emojis[i]
		text.strip()
	await bot.say(text)
	return

@bot.command(pass_context=False)
async def wc():
	status = sSurv.status()
	tt = "WhoCrafters Online"

	desc = "**Survival: "
	desc += format(status.players.online)
	desc += "**\n"
	badon = 0

	if (status.players.online > 0):
		for player in status.players.sample: #REDACTED
			if format(player.name) == "IGN here": #Ark
				desc += "pétoncule à la mode init"
			elif format(player.name) == "IGN here": #Nagi
				desc += "hmmm limiting :frog:"
			elif format(player.name) == "IGN here": #Tom
				desc += "one sexy boi :kiss:"
			else:
				desc += format(player.name)
			desc += "\n"
	else:
		desc += "empty init\n"

	status = sCrea.status()
	desc += "\n**Creative: "
	desc += format(status.players.online)
	desc += "**\n"

	if (status.players.online > 0):
		for player in status.players.sample:
			desc += format(player.name)
			desc += "\n"
	else:
		desc += "empty init\n"

	em = discord.Embed(title=tt,
	description=desc,
	colour=0xe74c3c)
	await bot.say(embed=em)

##### Bank Commands #####
def Spend(id, amt):
	r = SubtractBalance(GetBankIndex(id),amt)
	if (r == True):
		AddBalance(3, 500)
	return r
	
def SpendName(name, amt):
	r = SubtractBalance(GetNameIndex(id),amt)
	if (r == True):
		AddBalance(3, 25)
	return r
	
def SubtractBalance(user, amt):
	fbank = open (StrBank , "r")
	line = [line.rstrip('\n') for line in fbank]
	fbank.close()
	result = False
	
	if (int(line[user]) >= int(amt)):
		line[user] = int(line[user]) - int(amt)
		result = True
	
	f = open (StrBank , "w")
	for l in line:
		f.write("{}\n".format(l))		
	f.close()
	return result
	
def AddBalance(user, amt):
	fbank = open (StrBank , "r")
	line = [line.rstrip('\n') for line in fbank]
	fbank.close()
	
	line[user] = int(line[user]) + int(amt)
	
	f = open (StrBank , "w")
	for l in line:
		f.write("{}\n".format(l))		
	f.close()

def GetBankIndex(id): #REDACTED
	if (format(id) == "id here"): #toms id
		return 0
	if (format(id) == "id here"): #nugs id
		return 1
	if (format(id) == "id here"): #arks id
		return 2
		
	return 999

def GetNameIndex(name):
	if (format(name) == "tom"): #tom
		return 0
	if (format(name) == "nug"): #nug
		return 1
	if (format(name) == "ark"): #ark
		return 2
	if (format(name) == "ponkbot"): #ponkbot
		return 3
		
	return 999
	
def GetBalance(i):
	if (int(i) == 999):
		return 0

	fbank = open (StrBank , "r")
	line = [line.rstrip('\n') for line in fbank]
	bal = line[i]
	fbank.close()
	return bal
	
def GiveBalance(sender ,reciv, amt):
	fbank = open (StrBank , "r")
	result = 0
	line = [line.rstrip('\n') for line in fbank]
	sbal = int(line[sender])
	fbank.close()
	
	if (int(sbal) >= int(amt)):
		line[sender] = int(line[sender]) - int(amt)
		line[reciv] = int(line[reciv]) + int(amt)
				
		f = open (StrBank , "w")
		for l in line:
			f.write("{}\n".format(l))
			
		f.close()
		result = 1
		
	return result

@bot.command(pass_context=True)	
async def bal(ctx):
	myBal = GetBalance(GetBankIndex(ctx.message.author.id))
	await bot.say("You have {} Ponks".format(myBal))
	
@bot.command(pass_context=True)
async def balance(ctx):
	myBal = GetBalance(GetBankIndex(ctx.message.author.id))
	await bot.say("You have {} Ponks".format(myBal))	

@bot.command(pass_context=True)
async def give(ctx, user, amt):
	
	if (GetBankIndex(ctx.message.author.id) == 999):
		await bot.say("You don't have an account.")	
		return
	
	if (format(GetNameIndex(user)) == format(GetBankIndex(ctx.message.author.id))):
		await bot.say("thats you");
		return
		
	if (GetNameIndex(user) == 999):
		await bot.say("Can't find that user.")
		return
		
	if (amt == "0"):
		await bot.say(" ye ok m8.");
		return 
		
	r = GiveBalance(
		GetBankIndex(ctx.message.author.id),
		GetNameIndex(user),
		amt)
		
	if (r == 0):
		await bot.say("You don't have enough Ponks.")	
		return
	if (r == 1):
		await bot.say("You gave {} {} Ponks.".format(user, amt))		
		return
	
	await bot.say("wat")
	
@bot.command(pass_context=True)
async def lb(ctx):
	
	desc = ""
	fbank = open (StrBank , "r")
	line = [line.rstrip('\n') for line in fbank]
	board = [["Tom        ",int(line[0])], ["Nug         ", int(line[1])], ["Ark          ", int(line[2])], ["ponkbot", int(line[3])]]	
	board.sort(key=lambda x: x[1], reverse=True)
	fbank.close()
	
	total = int(line[0]) + int(line[1]) + int(line[2]) + int(line[3])
	for x in range(4):
		desc += "**"
		desc += format(board[x][0])
		desc += "** | "
		desc += "{:,}".format(board[x][1])
		desc += "\n"	
	
	em = discord.Embed(title="Ponk leaderboard", 
	description=desc, colour=0xe74c3c)
	em.set_footer(text="Total: {:,} ponks".format(total))

	await bot.say(embed=em)
	
@bot.command(pass_context=True)
async def take(ctx, user: discord.Member, amt):
	
	if (GetBankIndex(ctx.message.author.id) != 0):
		await bot.say("no.")	
		return
	
	if (format(user.id) == format(ctx.message.author.id)):
		return
		
	if (GetBankIndex(user.id) == 999):
		await bot.say("Can't find that user.")
		return
		
	if (amt == "0"):
		return 
		
	r = GiveBalance(GetBankIndex(user.id), 0, amt)
		
	if (r == 0):
		await bot.say("They dont have enough Ponks.")	
		return
	if (r == 1):
		await bot.say("You took {} Ponks from {}.".format(amt, format(user.name)))		
		return
	
	await bot.say("wat")
	
	
##### TESTING #####
@bot.command(pass_context=True)
async def happy(ctx, bday, name):
	if (bday != "birthday"):
		return
	if (name == "nug" or name == "nagi"):
		await bot.say(":tada:HAPPY:tada: BIRTHDAY:tada:NAGI!!!!:tada::birthday::frog:")
	return

@bot.command(pass_context=True)
async def slapmania(ctx, mode):
	global freeForAll
	if (mode == "on"):
		freeForAll = True
		await bot.say("Slap mania on!!")
	
	if (mode == "off"):
		freeForAll = False
		await bot.say("Slap mania off!!")

	return

@bot.command(pass_context=True)
async def yummo(ctx):
	if (GetBankIndex(ctx.message.author.id,) != 0):
		return
	
	desc = "```"
	desc += "Dirty spuds . . {:<6}\n".format(fallenMoney)
	desc += "Dog food  . . . {},{},{}\n".format(canGather[0],canGather[1],canGather[2])
	desc += "Milk  . . . . . {}\n".format(gatherLeft)
	desc += "Spaghetti . . . {}\n".format(pinataTime)
	desc += "Curried snags . {}\n".format(pinataHealth)
	desc += "burnt crepes  . {},{},{}\n".format(smacked[0],smacked[1],smacked[2])
	desc += "fish  . . . . . {}\n".format(freeForAll)
	desc += "```"	

	await bot.say(desc)
	

##### Interactive Commands #####
@bot.command(pass_context=False)
async def flip():
	i = random.randint(1,2)
	if i == 1:
		await bot.say("Heads")
	else:
		await bot.say("Tails")

@bot.command(pass_context=True)
async def roll(ctx, sides=6):
	if (int(sides) < 2 ):
		await bot.say("ye ok")
		return
	i = random.randint(1,sides)
	await bot.say("rolled a {}!".format(i))

@bot.command(pass_context=True)
async def guess(ctx, myGuess="help"):
	if  myGuess == "help":
		await bot.say("usage: *.guess <number>*\nGuess the number between 1 and 100")
		return

	if (Spend(ctx.message.author.id,5000) == False):
		await bot.say("You need 5000 ponks to guess")
		return

	if not myGuess.isdigit():
		await bot.say("gotta be a number m8")
		return

	i = random.randint(1,100)
	if int(myGuess) == i:
		await bot.say("The number is {}. You won 500,000 ponks!".format(i))
		AddBalance(GetBankIndex(ctx.message.author.id),500000)
	else:
		await bot.say("The number is {}. You lost 5,000 ponks!".format(i))

@bot.command(pass_context=True)
async def notes(ctx):
	fNotes = open (StrNotes , "r")
	notes = [line.rstrip('\n') for line in fNotes]

	totalChars = 0
	currentIndex = 0
	desc = "NOTES:\n```\n"
	for i in range(len(notes)):
		if totalChars + len(notes[i]) < 1800:
			totalChars += len(notes[i])
			desc += "{} {}\n".format(i+1, notes[i])
		else:
			desc += "```"
			await bot.say(desc)
			desc = "```\n"
			totalChars = 0
			desc += "{} {}\n".format(i+1, notes[i])
	desc += "```"

	await bot.say(desc)
	fNotes.close()
	return

@bot.command(pass_context=True)
async def addnote(ctx, msg):
	fNotes = open (StrNotes , "r")
	notes = [line.rstrip('\n') for line in fNotes]
	fNotes.close()

	notes.append(format(msg))

	f = open(StrNotes, "w")
	for n in notes:
		f.write("{}\n".format(n))
	f.close()

	await bot.say("added new note: \n{}".format(msg))
	return

@bot.command(pass_context=True)
async def delnote(ctx, lineNum):
	if not lineNum.isdigit():
		await bot.say("put a number there ok thanks")
		return

	fNotes = open (StrNotes , "r")
	notes = [line.rstrip('\n') for line in fNotes]
	fNotes.close()

	found = False
	f = open(StrNotes, "w")
	for i in range(len(notes)):
		if i != int(lineNum) - 1:
			f.write("{}\n".format(notes[i]))
		elif i == int(lineNum) - 1:
			found = True
	f.close()

	if found:
		await bot.say("Deleted note number: {}".format(lineNum))
	else:
		await bot.say("Could not find note number: {}".format(lineNum))
	return

@bot.command(pass_context=True)
async def snapnotes(ctx, arg=""):
	global confirmAsked
	if confirmAsked == False:
		await bot.say("Do you really want to snap notes?")
		confirmAsked = True
		return

	if arg == "confirm":
		await bot.say(":sparkles: mr ponk, my notes dont feel so good :sparkles:")

		fNotes = open(StrNotes, "r")
		notes = [line.rstrip('\n') for line in fNotes]
		fNotes.close()

		halfTotal = len(notes) / 2
		newlist = random.sample(notes,int(halfTotal))

		f = open(StrNotes, "w")
		for i in range(len(newlist)):
			f.write("{}\n".format(notes[i]))
		f.close()
		confirmAsked = False
	return

@bot.command(pass_context=True)
async def rnote(ctx):
	fNotes = open(StrNotes, "r")
	notes = [line.rstrip('\n') for line in fNotes]
	fNotes.close()

	n = random.randint(0,len(notes))
	await bot.say(format(notes[n]))
	return

async def DropChance(ctx, amt):
	global fallenMoney
	global canGather
	global gatherLeft
	global pinataTime
	global pinataHealth
	global smacked
	
	if (Spend(ctx.message.author.id,amt) == False):
		await bot.say("You dont have enough ponks")
		return False
	n = random.randint(1,100)
	
	if (n > 94):
		p = random.randint(301,599)
		fallenMoney += p
		canGather = [1,1,1]
		gatherLeft = 3
		await bot.say("{} ponks fell outta my ass".format(p))
	

	if (int(GetBalance(3)) > 30000):
		if (n < 10):
			await bot.say("IT'S PONKÑATA TIME!!")
			pinataTime = True
			pinataHealth = 4
			smacked = [0,0,0]
			return True
	if (int(GetBalance(3)) > 5000):
		if (n < 2):
			await bot.say("IT'S PONKÑATA TIME!!!")
			pinataTime = True
			pinataHealth = 2
			smacked = [0,0,0]
		
	return True

def BreakPinata():
	global fallenMoney
	global pinataHealth
	global pinataTime
	r = 0
	
	if (pinataHealth > 1):
		p = GetBalance(3)
		r = random.randint(75, int(int(p)/int(pinataHealth)))
	else:
		r = GetBalance(3)
		pinataTime = False
	
	pinataHealth -= 1
	SubtractBalance(3, int(r))
	fallenMoney += int(r)
	return r
	
@bot.command(pass_context=True)
async def sm(ctx, i):
	if (GetBankIndex(ctx.message.author.id,) != 0):
		return

	global smacked
	smacked[int(i)] = 1;
	
@bot.command(pass_context=True)
async def smack(ctx):
	global smacked
	global canGather
	global gatherLeft
	
	if (pinataTime == True):
		smacked[GetBankIndex(ctx.message.author.id)] = 1
		
		if (int(smacked[0]) + int(smacked[1]) + int(smacked[2]) == 3):
			cash = BreakPinata()
			
			if (pinataHealth == 3):
				await bot.say("PONKÑATAS ARM JUST FELL OFF AND DROPPED {} PONKS!".format(cash))
			if (pinataHealth == 2):
				await bot.say("YOU'VE CHOPPED PONKÑATAS LEG OFF! IT DROPPED {} PONKS!".format(cash))
			if (pinataHealth == 1):
				await bot.say("PONKÑATAS HEAD IS GONE! IT DROPPED {} PONKS!".format(cash))
			if (pinataHealth == 0):
				await bot.say("PONKÑATA GOT SMASHED TO BITS AND DROPPED {} PONKS!".format(cash))
			
			smacked = [0,0,0]
			canGather = [1,1,1]
			gatherLeft = 3

			
@bot.command(pass_context=True)
async def slap(ctx, name):
	global canGather
	global gatherLeft
	global fallenMoney
	global freeForAll
	n = int(GetNameIndex(name))
	u = int(GetBankIndex(ctx.message.author.id))
	
	if (u == n):
		await bot.say("You dropped 100")
		fallenMoney += 100
		return
	
	if (Spend(ctx.message.author.id,50) == False):
		await bot.say("You dont have enough ponks")
		return
	
	if (int(n) == 999):
		await bot.say("Swing and miss. You dropped 50")
		return 
		
	if (canGather[n] == 1 and freeForAll == False):
		await bot.say("You cant slap {} yet".format(name))
		return
		
	gatherLeft = 3
	fallenMoney += 25
	bal = GetBalance(GetNameIndex(name))
	
	if (int(bal) >= 50):
		SubtractBalance(n,50)
		fallenMoney += 50
		bal = 50
	else:
		SpendName(name,int(bal))
		fallenMoney += int(bal)
	
	canGather = [1,1,1]
		
	await bot.say("You dropped 25. {} dropped {}. There is currently {} ponks on the ground." .format(name ,bal , fallenMoney))
		
@bot.command(pass_context=True)
async def gather(ctx):	
	global canGather
	global gatherLeft
	global fallenMoney
	
	if (canGather[GetBankIndex(ctx.message.author.id)] == 0):
		await bot.say("You already gathered.")
		return 
	
	canGather[GetBankIndex(ctx.message.author.id)] = 0
	perc = 0
	if (gatherLeft > 1):
		perc = random.uniform(0,1)
		
	if (gatherLeft == 1):
		perc = 1;
	collected = int(round(perc * fallenMoney))
	AddBalance(GetBankIndex(ctx.message.author.id),collected)
	await bot.say("You gathered {} ponks." .format(collected))
	fallenMoney -= (collected)
	gatherLeft -= 1	

	
##### Text Commands #####
@bot.command(pass_context=True)
async def pasta(ctx, sub="ponk"):
	txt = "Every single day of my life I'm harassed by {}. The day I was born they busted in to my mother's hospital room and grabbed me away from my mother's hands and said to me \"That's {} to you kiddo.\" and they fell for hours away with their {} powers. Ever since then they have harassed me on a weekly basis. Don't trust {}, he's a monster.".format(sub, sub, sub, sub)
	await bot.say(txt)
	return

@bot.command(pass_context=True)
async def loose(ctx):	
	await bot.say("There is {} ponks on the ground." .format(round(fallenMoney)))

@bot.command(pass_context=True)
async def goodshit(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("/tts :ok_hand::eyes::ok_hand::eyes::ok_hand::eyes::ok_hand::eyes::ok_hand::eyes: good shit go౦ԁ sHit:ok_hand: thats :heavy_check_mark: some good:ok_hand::ok_hand:shit right:ok_hand::ok_hand:there:ok_hand::ok_hand::ok_hand: right:heavy_check_mark:there :heavy_check_mark::heavy_check_mark:if i do ƽaү so my self :100: i say so :100: thats what im talking about right there right there (chorus: ʳᶦᵍʰᵗ ᵗʰᵉʳᵉ) mMMMMᎷМ:100: :ok_hand::ok_hand: :ok_hand:НO0ОଠOOOOOОଠଠOoooᵒᵒᵒᵒᵒᵒᵒᵒᵒ:ok_hand: :ok_hand::ok_hand: :ok_hand: :100: :ok_hand: :eyes: :eyes: :eyes: :ok_hand::ok_hand:Good shit")

@bot.command(pass_context=True)
async def ayy(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("lmao")
		
@bot.command(pass_context=True)
async def yeok(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say(":thumbsup: :eggplant:")
	
@bot.command(pass_context=True)
async def dew(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("wanna stardew it?")
	
@bot.command(pass_context=True)
async def nug(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say(random.choice(nugArr))
	
@bot.command(pass_context=True)
async def ark(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say(":flag_gb: hey ark you pom init")
	
@bot.command(pass_context=True)
async def tom(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say(":flag_au: hey tom you rok m8")

@bot.command(pass_context=False)
async def map(arg = ""):
	if arg == "":
		await bot.say("https://cdn.discordapp.com/attachments/154607610493009920/520815556899766273/WC_MAP.png")
	elif arg == "g":
		await bot.say("https://cdn.discordapp.com/attachments/457457201506811907/525556320112345088/WC_MAP_G.png")
	elif arg == "eu":
		await bot.say("https://geology.com/world/europe-map.gif")
	elif arg == "au":
		await bot.say("https://geology.com/world/australia-map.gif")
	elif arg == "list":
		await bot.say('''MAPS:```
( )  -  Whocraft Map
(g)  -  Whocraft Map with 1k grid
(eu) -  Map of Europe
(au) -  Map of Australia
(<region>) - Map of region on geology.com 
```''')
	else:
		await bot.say("https://geology.com/world/{}-map.gif".format(arg))
	return

##### Video Commands #####
@bot.command(pass_context=True)
async def wakeup(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("https://www.youtube.com/watch?v=ooTORQv0O_Q")

@bot.command(pass_context=True)
async def ligma(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("https://www.youtube.com/watch?v=gFflmvcXHEk")

##### Giphy Commands #####
@bot.command(pass_context=True)
async def owo(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("https://www.tenor.co/t8Nt.gif")

@bot.command(pass_context=True)
async def noballs(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say(random.choice(noballsArr))

@bot.command(pass_context=True)
async def doo(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say(random.choice(dooArr))
	
@bot.command(pass_context=True)
async def doont(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("https://thumbs.gfycat.com/IcyBestHackee-size_restricted.gif")

@bot.command(pass_context=True)
async def nice(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("https://media.giphy.com/media/PhKhSXofSAm3e/giphy.gif")
	
@bot.command(pass_context=True)
async def ye(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say(random.choice(yeArr))
	
@bot.command(pass_context=True)
async def heh(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("https://media.giphy.com/media/u0LxmF9QVeDoQ/giphy.gif")
	
@bot.command(pass_context=True)
async def no(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("https://media.giphy.com/media/6gLyE15StAs3C/giphy.gif")
	
@bot.command(pass_context=True)
async def ponk(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("https://tenor.com/view/butthead-rock-beavis-gif-6281586")
	
@bot.command(pass_context=True)
async def pab(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say("https://media1.tenor.com/images/f2425e7c3dfe9dd47fcdcc89528c6b34/tenor.gif?itemid=4781957")
	
@bot.command(pass_context=True)
async def gottem(ctx):
	if (await DropChance(ctx, 50) == False):
		return
	await bot.say(random.choice(gottemArr))
	

##### Pokedex Commands #####
@bot.command(pass_context=True)
async def dex(ctx, c):
	tt = "Pokédex:"
	desc = ""
	for x in range(int(c) - 1, int(c) + 19):
		desc += "**"
		desc += format(myDex[x][0])
		desc += "** | "
		desc += format(myDex[x][1])
		
	em = discord.Embed(title=tt, 
	description=desc, 
	colour=0xe74c3c)
	em.set_footer(text="Displaying {}-{}".format(int(c), format(int(c) + 19)))
	await bot.say(embed=em)

@bot.command(pass_context=True)
async def dexr(ctx, a, b):
	tt = "Pokédex:"
	desc = ""
	for x in range(int(a) - 1, int(b)):
		desc += "**"
		desc += format(myDex[x][0])
		desc += "** | "
		desc += format(myDex[x][1])
		
	em = discord.Embed(title=tt, 
	description=desc, 
	colour=0xe74c3c)
	em.set_footer(text="Displaying {}-{}".format(int(a), format(int(b))))
	await bot.say(embed=em)

@bot.command(pass_context=True)
async def about(ctx):
	await bot.say("ponkbot v0.42.\nMade with hate by ilerm.\nThank you for breaking it all the time.")

##### Startup #####
@bot.event
async def on_ready():
	print ("I am running on " + bot.user.name)
	print ("with the ID: " + bot.user.id)

bot.run("bot id goes here") #REDACTED
