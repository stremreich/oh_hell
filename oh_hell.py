import random

suit_names = ["Spades", "Clubs", "Hearts", "Diamonds"]
card_vals = ["Two", "Three", "Four", "Five", \
			"Six", "Seven", "Eight", "Nine", "Ten", \
			"Jack", "Queen", "King", "Ace"]

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


c = Card(8,1)
c2 = Card(11,3)
d = Deck()

print(c2.suit)
print(c2.val)
print(c2.getName())
print(c2.getNameSh())

d.printOrderSh()
d.shuffle()
d.printOrderSh()