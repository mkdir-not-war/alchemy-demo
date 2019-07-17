from ingredients import ingredients, bases, brew

'''
actions:
	* heat (+1 heat level, -1 after 3 turns)
	* add
	* crush + add

'''

class Alchemy():
	def __init__(self):
		self.potions = []
		self.inputhandler = maininput
		self.base = None
		self.steps = {}
		for i in range(10):
			self.steps[i] = ('wait', None, None)
		self.possibleactions = ['add', 'crush and add', 'heat', 'wait']

	def reset(self):
		self.inputhandler = maininput
		self.base = None
		for i in range(10):
			self.steps[i] = ('wait', None, None)

def printsteps(alchemy):
	print("STEPS: ")
	print('\t', 'base', '\t', alchemy.base)
	for i in range(10):
		action = alchemy.steps[i][0]
		item = ''
		amount = ''
		if (not alchemy.steps[i][1] is None):
			item = alchemy.steps[i][1]
			amount = alchemy.steps[i][2]
		print('\t', i+1, '\t', action, item, amount)
	print('\t', '11', '\t', 'bottle it up!')

def brewinput(userinput, alchemy):
	if userinput == 'help':
		print('ingredients | actions | base | print | step N | brew | stop | quit')
	elif userinput == 'quit':
		exit(1)
	elif userinput == 'stop':
		alchemy.inputhandler = maininput
	elif userinput == 'ingredients':
		print("INGREDIENTS: ")
		for i in ingredients:
			print('\t', i)
	elif userinput == 'actions':
		print("ACTIONS: ")
		for i in alchemy.possibleactions:
			print('\t', i)
	elif userinput == 'base':
		baseinput = input('base: ')
		if baseinput not in ingredients:
			print("'%s' is not a viable base." % baseinput)
			print("bases: %s" % [name for name in bases])
		else:
			alchemy.base = baseinput
	elif userinput == 'print':
		printsteps(alchemy)
	elif userinput[:4] == 'step':
		splinput = userinput.split(' ')
		if (len(splinput) == 2):
			stepnum = int(splinput[1])
			if (stepnum < 1 or stepnum > 11):
				print("There is no step %s!" % stepnum)
				return
			elif (stepnum == 11):
				print("Step 11 is to bottle the concoction!")
				return
			stepnum = stepnum-1
			actioninput = input("action: ")
			if not actioninput in alchemy.possibleactions:
				print("'%s' is not a viable action." % actioninput)
				return
			if actioninput in ['wait', 'heat']:
				alchemy.steps[stepnum] = (actioninput, None, None)
				return
			iteminput = input("what do you want to %s?: " % actioninput)
			if not iteminput in ingredients:
				print("'%s' is not a viable ingredient." % iteminput)
				return
			amountinput = int(input("amount of %s: " % iteminput))
			if amountinput <= 0:
				print("You cannot %s %s amount of %s." % (
					actioninput, amountinput, iteminput))
				return
			alchemy.steps[stepnum] = (actioninput, iteminput, amountinput)

	elif userinput == 'brew':
		if (not alchemy.base is None):
			base_ingredient = ingredients[alchemy.base]
			potion = brew(base_ingredient, alchemy.steps)
			alchemy.potions.append(potion)
			print(potion.name)
			potion.printeffects()
			alchemy.inputhandler = maininput
			alchemy.reset()
		else:
			print('You need a base before you brew the potion.')
	else:
		brewinput('help', alchemy)

def maininput(userinput, alchemy):
	if userinput == 'help':
		print('clear | potions | brew | quit')
	elif userinput == 'clear':
		alchemy.potions.clear()
		print("Cleared potions.")
	elif userinput == 'potions':
		if (len(alchemy.potions)<=0):
			print("No potions.")
			return
		print()
		print("POTIONS: ")
		for p in range(len(alchemy.potions)):
			print('~ %s ~' % (alchemy.potions[p].name))
			print(alchemy.potions[p].compounds)
			alchemy.potions[p].printeffects()
			print('-' * 12)
			print()
	elif userinput == 'brew':
		alchemy.inputhandler = brewinput
	elif userinput == 'quit':
		exit(1)
	else:
		maininput('help', alchemy)

def main():
	alchemy = Alchemy()
	while(1):
		userinput = input('>> ')
		alchemy.inputhandler(userinput, alchemy)

if __name__=='__main__':
	main()