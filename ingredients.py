from numpy import dot
from operator import itemgetter
import compounds
from effects import alleffects, EffectType
from string import ascii_uppercase as compound_names

def squaredlen(vec):
	result = 0
	for d in vec:
		result += d ** 2
	return result

def effect_ingredient_similarity(target, size):
	square_cos = {}
	sqlen_target = squaredlen(target)
	for e in alleffects.values():
		effect_vector = tuple(e.vector)
		dotprod = dot(effect_vector, target)
		value = (dotprod * dotprod) / \
			(squaredlen(effect_vector) * sqlen_target)
		if (not value in square_cos):
			square_cos[value] = [e]
		else:
			square_cos[value].append(e)

	scores_nodup = sorted(square_cos, reverse=True)
	scores = []
	for s in scores_nodup:
		for i in range(len(square_cos[s])):
			scores.append(s)
	effects = []
	for s in scores_nodup:
		effects.extend(square_cos[s])
	return scores[:size], effects[:size]

def potency(compounds, signature):
	# mask out signature from compounds
	values = []
	for c in compounds:
		if c in signature:
			values.append(compounds[c])
	# find minimum value among masked compounds
	if not values:
		return 0
	return min(values)

class Ingredient():
	def __init__(self, name, compounds, crushed=None, base=False):
		self.name = name
		self.compounds = compounds.copy() # {name : amount}
		self.effects = self.calculateeffects(compounds)
		self.base = base

		if crushed is None:
			crushed = self.name
		self.crushed = crushed

		if len(name) >= 6 and name[-6:] == "potion":
			self.name = self.namepotion(name)


	def calculateeffects(self, compounds):
		max_effects_per_ingredient = 3
		result = {} # [(effect, potency), ...]
		compound_vector = [compounds[i] 
							if i in compounds.keys() else 0 
							for i in list(compound_names)]	
		scores, effects = effect_ingredient_similarity(
			tuple(compound_vector), max_effects_per_ingredient)
		for e_index in range(len(effects)):
			effect = effects[e_index]
			compound_potency = potency(compounds, effect.signature)
			effect_potency = int(max((10.0 * (compound_potency) * \
				scores[e_index]), 0))
			if (effect.effecttype == EffectType.NEGATIVE):
				effect_potency *= -1
			# sum up negative and positive effects
			if (effect_potency != 0):
				if (effect.stat in result):
					result[effect.stat][1] += effect_potency
					if (result[effect.stat][1]) == 0:
						del result[effect.stat]
				else:
					result[effect.stat] = [effect, effect_potency]
		return result

	def namepotion(self, basename):
		effectslist = sorted(
			list(self.effects.items()),
			key=lambda e: e[1][1],
			reverse=True)
		if (len(effectslist) == 0):
			return 'inert potion of %s' % basename[:-7]
		max_pos_effects = []
		min_neg_effects = []
		max_potency = 0
		min_potency = 0
		for e in effectslist:
			potency = e[1][1]
			if potency > max_potency:
				max_potency = potency
				max_pos_effects = [e[0]]
			elif potency == max_potency:
				max_pos_effects.append(e[0])
			if potency < min_potency:
				min_potency = potency
				min_neg_effects = [e[0]]
			elif potency == min_potency:
				min_neg_effects.append(e[0])

		if (abs(min_potency) > max_potency):
			basename = basename[:-6] + 'poison'
			name = '%s of deplete %s' % (basename, ' and '.join(min_neg_effects))
		else:
			name = '%s of augment %s' % (basename, ' and '.join(max_pos_effects))

		return name

	def crush(self):
		result = ingredients[self.crushed]
		return result

	def printeffects(self):
		for effect, potency in self.effects.values():
			print("%s: %s" % (effect.stat, str(potency)))

# base = Ingredient
# steps = [(<action>, <ingredient>/None)]
def brew(base, steps):
	compoundsdict = base.compounds.copy()

	max_heat = compounds.heatlevels['hot'][0] # minimum heat = 0
	stepsperheat = 3

	heattimer = 0
	heatlevel = 0
	turnsabovetemp = [0] * (max_heat)

	for stepnum in range(10):
		step = steps[stepnum]
		action, item, amount = step
		# 1) destroy compounds that hit their tolerance
		destroyedcompounds = []
		for c in compoundsdict:
			compound = compounds.allcompounds[c]
			if not compound.max_temp is None:
				if turnsabovetemp[compound.max_temp] >= 2:
					destroyedcompounds.append(c)
		for c in destroyedcompounds:
			del compoundsdict[c]

		# 2) apply add and crush actions, if applicable
		if (action in ['add', 'crush and add']):
			itemingredient = ingredients[item]
			if action == 'crush and add':
				itemingredient = itemingredient.crush()
			for compound in itemingredient.compounds:
				amt = itemingredient.compounds[compound] * amount
				if (compound in compoundsdict):
					compoundsdict[compound] += amt
				else:
					compoundsdict[compound] = amt

		# 3) resolve any reactions in order of reactivity
		compoundlist = sorted(
			list(compoundsdict.items()),
			key=lambda c: compounds.allcompounds[c[0]].reactivity,
			reverse=True)
		compoundlist = [c for c in compoundlist \
			if compounds.allcompounds[c[0]].reactivity >= 0]
		'''
		NOTE: when two compounds react, 
		the result's amount is double the minimum
		of the amounts of the two compounds, 
		with the greater amount having leftover
		'''
		reacting = []
		for compound, amount in compoundlist:
			heattier = compounds.heatlevels[heatlevel]
			reactions = None
			if heattier == 'cold':
				reactions = compounds.allcompounds[compound].cold_reactions
			elif heattier == 'warm':
				reactions = compounds.allcompounds[compound].warm_reactions
			elif heattier == 'hot':
				reactions = compounds.allcompounds[compound].hot_reactions
			for r in reactions:
				if r in compoundsdict:
					reacting.append((compound, r, reactions[r],
						min(amount, compoundsdict[r])))
		new_compounds = {}
		for r1, r2, result, amount in reacting:
			if (r1 in compoundsdict and r2 in compoundsdict):
				if (compoundsdict[r1] > compoundsdict[r2]):
					del compoundsdict[r2]
					compoundsdict[r1] -= amount
				elif (compoundsdict[r1] < compoundsdict[r2]):
					del compoundsdict[r1]
					compoundsdict[r2] -= amount
				else:
					# equal amounts, delete both
					del compoundsdict[r1]
					del compoundsdict[r2]
				new_compounds[result] = amount * 2
		compoundsdict.update(new_compounds)


		# 4) update heat level and turns above temp
		for i in range(0, min(heatlevel, max_heat)):
			turnsabovetemp[i] += 1
		for i in range(heatlevel+1, max_heat):
			turnsabovetemp[i] = 0
		if (action == 'heat'):
			if (heatlevel < max_heat):
				heatlevel += 1
			heattimer = stepsperheat
		heattimer -= 1
		if (heattimer == 0):
			if (heatlevel > 0):
				heatlevel -= 1
			heattimer = stepsperheat

	result = Ingredient("%s potion" % base.name, compoundsdict, base=True)
	return result

# should this even be a possible action?
def distill(compoundlist):
	new_compounds = {}
	for c in compoundlist:
		# reactivity -1 -> 0: remove the compound
		mult = (compounds.allcompounds[c].reactivity + 1)
		new_compounds[c] = compoundlist[c] * mult
	return new_compounds

ingredients = {
	# bases
	'water' : Ingredient("water", {'A':1, 'B':1, 'C':1, 'D':1}, 
		base=True),
	'blood' : Ingredient("blood", {'D':2, 'E':2, 'G':1, 'H':1}, 
		base=True),
	'slime' : Ingredient("slime", {'H':1, 'I':1, 'K':2, 'S':1}, 
		base=True),
	'ectoplasm' : Ingredient("ectoplasm", {'H':1, 'I':1, 'L':2, 'N': 2}, 
		base=True),
	# from corpses
	'bone' : Ingredient("bone", {'A':1, 'E':1}, 
		crushed="crushed bone"),
	'crushed bone' : Ingredient("crushed bone", {'A':1, 'E':1, 'M':1}),
	'troll eye' : Ingredient("troll eye", {'F':2, 'H':1, 'I':1, 'K':1}, 
		crushed="slime"), 
	'orc ear' : Ingredient("orc ear", {'F':1, 'G':1, 'J':1}, 
		crushed="blood"),
	'kobold tooth' : Ingredient("kobold tooth", {'A':1, 'C':2, 'E':2, 'H':1}, 
		crushed="crushed bone"),
	'dragon scale' : Ingredient("dragon scale", {'B':1, 'C':2, 'D':1, 'I':1}, 
		crushed="powdered scale"),
	'fish scale' : Ingredient("fish scale", {'B':2, 'I':2, 'J':1}, 
		crushed="powdered scale"),
	'powdered scale' : Ingredient("powdered scale", {'B':2, 'C':2, 'I':2}, 
		crushed="blood"),
	# plants
	'drake thistle' : Ingredient("drake thistle", {'C':1, 'E':1, 'G':1, 'H':2}),
	'milkweed' : Ingredient("milkweed", {'C':1, 'F':1, 'H':2, 'O':1})
}

bases = {k:v for (k,v) in ingredients.items() if v.base}

def printingredients():
	for i in ingredients:
		print('~', i, '~')
		ingredients[i].printeffects()
		print('-'*12)

def printtestpot():
	pot_comp = {'A':2, 'C':4, 'E':4, 'H':2}
	test_pot = Ingredient('test potion', pot_comp, base=True)
	print(test_pot.name)
	test_pot.printeffects()

	test_pot.compounds = distill(test_pot.compounds)
	test_pot.calculateeffects(test_pot.compounds)
	print('distilled '+ test_pot.name)
	test_pot.printeffects()

if __name__=='__main__':
	printtestpot()
	#printingredients()
