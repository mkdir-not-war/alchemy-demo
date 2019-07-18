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
		self.inputhandler = brewinput
		self.base = None
		self.steps = {}
		for i in range(10):
			self.steps[i] = ('wait', None, None)
		self.possibleactions = ['add', 'crush and add', 'heat', 'cool', 'wait']

	def reset(self):
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

helptext = """ commands:
	potions \t- view all potions and their effects
	clear \t\t- clear all potions
	print \t\t- view base and steps in current recipe
	new \t\t- clear base and steps in current recipe
	base \t\t- enter a base into the current recipe 
	\t\t(will overwrite)
	ingredients \t- view names of all ingredients
	actions \t- view all possible actions in a step
	step N \t\t- prompts an action, ingredient and 
	\t\tamount if applicable for step N 
	\t\t(will overwrite)
	brew \t\t- execute the steps in the current recipe, 
	\t\tadds the potion to potions and starts a new recipe
	help \t\t- bring up this menu
	quit \t\t- exit the program
"""

def brewinput(userinput, alchemy):
	if userinput == 'help':
		print(helptext)
	elif userinput == 'quit':
		return True
	elif userinput == 'ingredients':
		print("INGREDIENTS: ")
		for i in ingredients:
			base = '[base]' if i in bases else ''
			print('\t', i, base)
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
				return False
			elif (stepnum == 11):
				print("Step 11 is to bottle the concoction!")
				return False
			stepnum = stepnum-1
			actioninput = input("action: ")
			if not actioninput in alchemy.possibleactions:
				print("'%s' is not a viable action." % actioninput)
				return False
			if actioninput in ['wait', 'heat', 'cool']:
				alchemy.steps[stepnum] = (actioninput, None, None)
				return False
			iteminput = input("what do you want to %s?: " % actioninput)
			if not iteminput in ingredients:
				print("'%s' is not a viable ingredient." % iteminput)
				return False
			amountinput = int(input("amount of %s: " % iteminput))
			if amountinput <= 0:
				print("You cannot %s %s amount of %s." % (
					actioninput, amountinput, iteminput))
				return False
			alchemy.steps[stepnum] = (actioninput, iteminput, amountinput)

	elif userinput == 'brew':
		if (not alchemy.base is None):
			base_ingredient = ingredients[alchemy.base]
			potion = brew(base_ingredient, alchemy.steps)
			alchemy.potions.append(potion)
			print(potion.name)
			potion.printeffects()
			alchemy.reset()
		else:
			print('You need a base before you brew the potion.')
	elif userinput == 'clear':
		if (len(alchemy.potions)<=0):
			print("No potions.")
			return False
		alchemy.potions.clear()
		print("Cleared potions.")
	elif userinput == 'new':
		alchemy.reset()
		print("Cleared current recipe.")
	elif userinput == 'potions':
		if (len(alchemy.potions)<=0):
			print("No potions.")
			return False
		print()
		print("POTIONS: ")
		for p in range(len(alchemy.potions)):
			print('~ %s ~' % (alchemy.potions[p].name))
			print(alchemy.potions[p].compounds)
			alchemy.potions[p].printeffects()
			print('-' * 12)
			print()
	else:
		print(helptext)
	return False

def main():
	alchemy = Alchemy()
	print(helptext)
	quit = False
	while(not quit):
		userinput = input('>> ')
		quit = alchemy.inputhandler(userinput, alchemy)

if __name__=='__main__':
	main()