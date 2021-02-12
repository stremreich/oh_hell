import random

suit_names = ["Spades", "Clubs", "Hearts", "Diamonds"]
card_vals = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]

class Card:
	suit = 0
	val = 0

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

class Deck:
	order = []

	def __init__(self):
		self.order = [Card(val, suit) for val in range(13) for suit in range(4)] 

	def shuffle(self):
		random.shuffle(self.order)

	def printOrder(self):
		for it in range(52):
			print(self.order[it].getName())

	def printOrderSh(self):
		print("----")
		for it1 in range(4):
			line = ""
			for it2 in range(13):
				line += self.order[it1*13 + it2].getNameSh()
				line += " "
			print(line)
		print("----")

class Player:
	name = ""
	hand = []
	score = 0

	def __init__(self):
		self.name = "Player"
		self.score = 0

	def __init__(self, name):
		self.name = name
		self.score = 0

	def printPlayerInfo(self):
		print('Info for player %s' % self.name)
		print('Score: %d' % self.score)
		print('Hand contents:')
		for card in self.hand:
			print(card.getName())



class Game:
	players = []
	hook = True
	maxHands = 7
	deck = Deck()

	def __init__(self, pNames, nHands, hookBool):
		self.maxHands = nHands
		self.hook = hookBool
		self.deck = Deck()
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
			print('%s: %d' % (player.name, player.score))
		print('Deck contents: ')
		self.deck.printOrderSh()
		
	def play(self):
		#TODO: implement oh hell! game rules


c = Card(8,1)
c2 = Card(11,3)
d = Deck()
p = Player("testPlayer")
p.hand = [c, c2]

p.printPlayerInfo()

pN = ['STR', 'ETR', 'Mom', '3P', 'PJ', 'CJ']

g = Game(pN, 7, True)
g.printGameInfo()

