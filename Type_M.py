import keyboard as kb
import random ,json
from time import time, sleep
from threading import Thread
from colorama import  Fore


def showLeaderBoard():
	global jsondata
	sleep(2)
	print()
	print(Fore.GREEN+'NAME\t\tWORDS\t\tTIME(sec)\tWPM'+Fore.RESET)
	print(Fore.RED+'='*60+Fore.RESET)

	sorted_list=sorted(jsondata,key=lambda key : jsondata[key]['wpm'] ,reverse=True)

	for key in sorted_list:
		print('{}\t\t{}\t\t{}\t\t{}'.format(jsondata[key]['name'],jsondata[key]['words'],jsondata[key]['time'],jsondata[key]['wpm']))
	


def monitorForQuit(p1):
	global end_flag
	while(True):
		if(kb.is_pressed('ctrl+q')):
			#print('User tried to quit')
			end_flag=1
			break
	p1.end_time=time()
	p1.playtime=int(p1.end_time-p1.start_time)
	p1.wpm=p1.words*60//p1.playtime

	# Write the necessary data of current player to jsondata.

	jsondata["P"+str(players)]['name']=p1.name
	jsondata["P"+str(players)]['words']=p1.words
	jsondata["P"+str(players)]['time']=p1.playtime
	jsondata["P"+str(players)]['wpm']=p1.wpm

	showLeaderBoard()		

	print('\nHIT ENTER')

def getUserInput(p1):
	global end_flag
	print('Start typing the paragraph shown to you. Press Ctrl+Q to exit')
	p1.start_time=time()
	

	while(True):
		
		if(end_flag==1):
			print('Your turn finished !!')
			break

		# Display the paragraph to the user.
		current_sentence=random.choice(content).strip()
		print()
		print(Fore.BLUE+current_sentence+Fore.RESET)

		# Get the user input.
		user_inp=input()

		current_sentence_words=current_sentence.split()
		user_typed_words=user_inp.split()

		for user_given in user_typed_words:
			if(user_given in current_sentence_words):
				p1.words+=1

		print()


class Player:
	def __init__(self,name):
		self.name=name
		self.words=0
		self.start_time=0
		self.end_time=0
		self.wpm=0

game_run=1
para_g=open('paragraph.txt','r')
content=para_g.readlines()


# Read the JSON data that is already saved.
fr=''										# File read pointer
try:
	fr=open('scorecard.json','r')
	jsondata=json.loads(fr.read())
except:
	fr=open('scorecard.json','w+')			# If scorecard.json doesn't exit, create it.
	fr.write("{}")							# Write the basic JSON structure of {} to it
	fr.seek(0)								# Move the pointer to SOF.
	jsondata=json.loads(fr.read())			# Read the data from it.

players=len(jsondata)						# Total number of players present in scorecard
fr.close()

# Type master game begins here...
while(game_run):

	end_flag=0

	player=input('Enter your name : ')			#get name input here 	
	p1=Player(player)                       
	
	players+=1									# Increment players, as a new player will play the game
	jsondata['P'+str(players)]={}				# Create empty dictionary for the new player


	t1=Thread(target=getUserInput,args=(p1,))
	t1.start()


	t2=Thread(target=monitorForQuit,args=(p1,))
	t2.start()

	t1.join()
	t2.join()

	print()
	print('1. Play another game')
	print('2. Quit game')
	option=input('Enter your option : ')

	if(option=='2'):
		game_run=0
	elif(option=='1'):
		pass
	else:
		print('You have entered invalid option.')
		print('Game will end')
		break
	print()

para_g.close()

# Save the stats of all the players.

fsw=open('scorecard.json','w')					# File write pointer
json.dump(jsondata,fsw,indent=4)
fsw.close()

print('Data saved successfully.')
