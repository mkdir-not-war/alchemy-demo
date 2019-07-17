from string import ascii_uppercase as compound_names
from enum import Enum

class EffectType(Enum):
	POSITIVE = 1
	NEGATIVE = 2

class Effect():
	def __init__(self, stat, signature, effecttype):
		self.stat = stat
		'''
		Each effect's signature is 3 compounds (names), 
		and implies equal amounts of each. Basically a bit-
		vector with exactly three 1's.

		Effects that have only compounds that occur in nature means
		eating raw ingredients can potentially yield that effect
		with high potency.
		'''
		self.signature = signature
		self.vector = self.effectvector()
		self.effecttype = effecttype

	def effectvector(self):
		result = [1 if i in self.signature else 0 \
			for i in compound_names]
		return result

alleffects = {
	'+hp' : Effect('hp', 				['A', 'D', 'M'],
		EffectType.POSITIVE),
	'+stamina' : Effect('stamina', 		['A', 'B', 'O'],
		EffectType.POSITIVE),
	'+speed' : Effect('speed', 			['C', 'O', 'S'],
		EffectType.POSITIVE),
	'+defense' : Effect('defense', 		['A', 'M', 'T'],
		EffectType.POSITIVE),
	'+spdefense' : Effect('spdefense', 	['E', 'G', 'N'],
		EffectType.POSITIVE),
	'+attack' : Effect('attack', 		['B', 'F', 'W'],
		EffectType.POSITIVE),
	'+spattack' : Effect('spattack', 	['E', 'K', 'X'],
		EffectType.POSITIVE),
	'+heat' : Effect('heat', 			['C', 'U', 'V'],
		EffectType.POSITIVE),
	'-hp' : Effect('hp', 				['E', 'H', 'P'],
		EffectType.NEGATIVE),
	'-stamina' : Effect('stamina', 		['F', 'J', 'R'],
		EffectType.NEGATIVE),
	'-speed' : Effect('speed', 			['D', 'I', 'N'],
		EffectType.NEGATIVE),
	'-defense' : Effect('defense', 		['I', 'N', 'W'],
		EffectType.NEGATIVE),
	'-spdefense' : Effect('spdefense', 	['J', 'R', 'T'],
		EffectType.NEGATIVE),
	'-attack' : Effect('attack', 		['H', 'K', 'S'],
		EffectType.NEGATIVE),
	'-spattack' : Effect('spattack', 	['D', 'G', 'P'],
		EffectType.NEGATIVE),
	'-heat' : Effect('heat', 			['B', 'Q', 'X'],
		EffectType.NEGATIVE),
	'invis' : Effect('invisibility', 	['L', 'V', 'X'],
		EffectType.POSITIVE)
}
	