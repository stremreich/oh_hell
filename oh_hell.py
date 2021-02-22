import random
import itertools

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
		evalList = list(itertools.compress(cardList, trumpList))
	else:
		evalList = list(itertools.compress(cardList, followSuitList))
	
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

	def __init__(self, *args, **kwargs):
		if (len(args) == 0):
			self.name = "Player"
		else:
			self.name = args[0]
		
		self.score = 0
		self.hand = []

	def printPlayerInfo(self):
		print('Info for player %s' % self.name)
		print('Score: %d' % self.score)
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
			print('%s: %d' % (player.name, player.score))
		print('Deck contents: ')
		self.deck.printOrderSh()
		
	def play(self):
		handNums = list(range(self.maxHands, 0 , -1)) + list(range(2, self.maxHands + 1))
		for hand in handNums: #hand loop
			self.deck.shuffle()
			for _ in range(hand):  #deal cards
				for i, player in enumerate(self.players):
					self.players[i].hand.append(self.deck.order.pop())
			trumpCard = self.deck.order.pop()  #turn trump card face-up
			bids = [0] * len(self.players)  # make bids TODO: make this controlled by a changeable decision function
			sumbids = 0
			for i in range(len(bids)):
				bids[i] = random.randint(0, 2) # just give a random bid for now TODO: make generalized
				sumbids += bids[i]
			if (sumbids == hand and self.hook): #enforce the hook, this should be handled in the method above eventually
				bids[len(self.players) - 1] += 1


			for trick in range(0, len(self.players[0].hand)): #loop through all tricks in a hand
				playedCards = []	

				for player in self.players:
					print("Trick %d:" % (trick + 1))
					#Play lead card, dealer is the last player in self.players
					if player == self.players[0]: 
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
							playedCards.append(player.hand.pop(random.randint(0, len(player.hand))))
						
				wonCard = cardEval(playedCards, trumpCard)
				print("%s was the best card." % wonCard.getName())
				#TODO: eval who won the trick, maybe compartmentalize trick a bit more? only need a list of players and their trick score...
				#TODO: change who leads based on who won the trick, maybe do this with pointers, itertools.cycle()

			self.players.append(self.players.pop(0)) #change dealer at the end of the hand, maybe also do this with itertools.cycle


c = Card(8,1)
c2 = Card(11,3)
d = Deck()
p = Player("testPlayer")
p.hand = [c, c2]

p.printPlayerInfo()

pN = ['STR', 'ETR', 'Mom', '3P', 'PJ', 'CJ']

g = Game(pN, 7, True)
g.printGameInfo()
g.play()

