import random
from itertools import islice, cycle, compress
import csv

suit_names = ["Spades", "Clubs", "Hearts", "Diamonds"]
card_vals = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]

def cardEval(cardList, trumpCard):

	trumpList = [0]*len(cardList)
	followSuitList = [0]*len(cardList)
	hasTrump = False
	for i, card in enumerate(cardList):
		if (card.suit == trumpCard.suit):
			hasTrump = True
			trumpList[i] = 1
		if (card.suit == cardList[0].suit):
			followSuitList[i] = 1

	if(hasTrump):
		evalList = list(compress(cardList, trumpList))
	else:
		evalList = list(compress(cardList, followSuitList))
	
	if (not len(evalList)): #if there's only one card left, return it
		return evalList[0]

	tempCard = evalList[0] #find highest value card among remaining
	for card in evalList[1:]:
		if (card.val > tempCard.val):
			tempCard = card

	return tempCard

class Card:

	def __init__(self, val, suit):
		self.suit = suit
		self.val = val

	def getName(self):
		return card_vals[self.val] + " of " + suit_names[self.suit] 

	def getNameSh(self):
		if self.val < 9: #Not a face card
			return str(self.val + 2) + suit_names[self.suit][0]
		else:
			return card_vals[self.val][0] + suit_names[self.suit][0]

	def isLegal(self, lead, trump):
		return (self.suit == lead.suit) or (self.suit == trump.suit) 

class Deck:

	def __init__(self):
		self.order = [Card(val, suit) for val in range(13) for suit in range(4)] 

	def shuffle(self):
		random.shuffle(self.order)

	def printOrder(self):
		for it in range(52):
			print(self.order[it].getName())

	''' # Needs to be re-made for non-full deck, do if needed...
	def printOrderSh(self):
		print("----")
		for it1 in range(4):
			line = ""
			for it2 in range(13):
				line += self.order[it1*13 + it2].getNameSh()
				line += " "
			print(line)
		print("----")
	'''

class Player:

	def __init__(self, *args, **kwargs):
		if (len(args) == 0):
			self.name = "Player"
		else:
			self.name = args[0]
		
		self.gameScore = 0
		self.trickScore = 0
		self.bid = 0
		self.hand = []

	def printPlayerInfo(self):
		print('Info for player %s' % self.name)
		print('Score: %d' % self.gameScore)
		print('Hand contents:')
		for card in self.hand:
			print(card.getName())

class Game:

	def __init__(self, pNames, nHands, hookBool):
		self.maxHands = nHands
		self.hook = hookBool
		self.deck = Deck()
		self.deck.shuffle()
		self.players = []
		for name in pNames:
			self.players.append(Player(name))

	def printGameInfo(self):
		print('Game Info: ')
		#print('Number of players: %d' % len(self.playerNames))
		#print('Players:')
		#for pName in self.playerNames:
		#  	print(pName)
		print('Maximum starting cards: %d' % self.maxHands)
		#print('Maximum possible starting cards: %d' % int(52 / len(self.playerNames)))
		print('Player Scores: ')
		for player in self.players:
			print('%s: %d' % (player.name, player.gameScore))
		#print('Deck contents: ')
		#self.deck.printOrderSh()
		
	def play(self):
		handNums = list(range(self.maxHands, 0 , -1)) + list(range(2, self.maxHands + 1))
		dealers = list(islice(cycle(self.players), 0, len(handNums)))  # make list of all dealers for all hands
		for handIndex, handLength in enumerate(handNums): #hand loop; handIndex is the nth hand and handLength is the tricks in the hand
			self.deck = Deck() #re-fill deck
			self.deck.shuffle() #shuffle
			for i in range(handLength):  #deal cards
				for j, player in enumerate(self.players):
					if (i == 0): #reset bids and trick scores
						self.players[j].bid = 0
						self.players[j].trickScore = 0
					self.players[j].hand.append(self.deck.order.pop())
			trumpCard = self.deck.order.pop()  #turn trump card face-up
			#bids = [0] * len(self.players)  # make bids TODO: make this controlled by a changeable decision function
			sumbids = 0
			for player in self.players:
				player.bid = random.randint(0, 2) # just give a random bid for now TODO: make generalized
				sumbids += player.bid
			if (sumbids == handLength and self.hook): #enforce the hook, this should be handled in the method above eventually
				self.players[-1].bid += 1

			dealer = dealers[handIndex]
			dealerIndex = self.players.index(dealer)
			trickOrder = list(islice(cycle(self.players), dealerIndex, dealerIndex + len(self.players))) #set up the initial trick order
			for trick in range(handLength): #loop through all tricks in a hand
				print("Trick %d:" % (trick + 1))
				playedCards = []	

				for player in trickOrder:
					#Play lead card
					if player == trickOrder[0]: 
						playedCards.append(player.hand.pop(random.randint(0, len(player.hand) - 1)))
					else:
						# must play only legal cards
						# play the first legal card
						played = False
						for card in player.hand:
							if card.isLegal(playedCards[0], trumpCard):
								playedCards.append(card)
								player.hand.remove(card)
								played = True
								break
						if(not played): #if there's no legal card, play a random card
							playedCards.append(player.hand.pop(random.randrange(len(player.hand))))
					
					print("{} played {}".format(player.name, playedCards[-1].getName()))
				
				# evaluate winner, increment trick score
				wonCard = cardEval(playedCards, trumpCard)
				wonPlayer = trickOrder[playedCards.index(wonCard)]
				print("{} won the trick with the {}".format(wonPlayer.name, wonCard.getName()))
				wonPlayer.trickScore += 1
				
				#re-make the trick order based on winner of this trick
				playersIndex = self.players.index(wonPlayer)
				trickOrder = list(islice(cycle(self.players), playersIndex, playersIndex + len(self.players)))
			
			#evaluate bids and increment game scores
			print("Evaluating bids for hand {}:".format(handIndex))
			for player in self.players:
				if player.trickScore == player.bid:
					player.gameScore += 10 + player.trickScore
					print("{} took {} tricks and bid {}. +{} points".format(player.name, player.trickScore, player.bid, 10 + player.trickScore))
				else:
					player.gameScore += player.trickScore
					print("{} took {} tricks and bid {}. +{} points".format(player.name, player.trickScore, player.bid, player.trickScore))
		
		print("Final Scores:")
		for player in self.players:
			print("{} - {}".format(player.name, player.gameScore))

def runTest(numGames, pNames, nHands, hook):
	with open('gameData.csv', mode='w', newline='') as dataFile:
		dataWriter = csv.writer(dataFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		titleRow = ['Game #'] + pNames
		dataWriter.writerow(titleRow)

		for i in range(numGames):
			g = Game(pNames, nHands, hook)
			g.play()
			g.printGameInfo()
			dataRow = [i]
			for player in g.players:
				dataRow.append(player.gameScore)
			dataWriter.writerow(dataRow)


'''
c = Card(8,1)
c2 = Card(11,3)
d = Deck()
p = Player("testPlayer")
p.hand = [c, c2]

p.printPlayerInfo()
'''

pN = ['STR', 'ETR', 'Mom', '3P', 'PJ', 'CJ']
#g = Game(pN, 7, True)
#g.printGameInfo()
#g.play()
#g.printGameInfo()

runTest(100, pN, 7, True)
