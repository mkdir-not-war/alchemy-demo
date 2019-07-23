from string import ascii_uppercase as compound_names
from enum import Enum

class EffectType(Enum):
	RESTORE = 1
	DEPLETE = 2
	BUFF = 3
	DEBUFF = 4

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
		EffectType.RESTORE),
	'+speed' : Effect('speed', 			['C', 'O', 'S'],
		EffectType.BUFF),
	'+defense' : Effect('defense', 		['J', 'M', 'T'],
		EffectType.BUFF),
	'+spdefense' : Effect('spdefense', 	['E', 'G', 'N'],
		EffectType.BUFF),
	'+attack' : Effect('attack', 		['B', 'F', 'W'],
		EffectType.BUFF),
	'+spattack' : Effect('spattack', 	['E', 'K', 'X'],
		EffectType.BUFF),
	'+heat' : Effect('heat', 			['C', 'U', 'V'],
		EffectType.BUFF),

	'-hp' : Effect('hp', 				['F', 'H', 'P'],
		EffectType.DEPLETE),
	'-speed' : Effect('speed', 			['D', 'I', 'N'],
		EffectType.DEBUFF),
	'-defense' : Effect('defense', 		['I', 'O', 'W'],
		EffectType.DEBUFF),
	'-spdefense' : Effect('spdefense', 	['J', 'R', 'T'],
		EffectType.DEBUFF),
	'-attack' : Effect('attack', 		['H', 'K', 'S'],
		EffectType.DEBUFF),
	'-spattack' : Effect('spattack', 	['D', 'G', 'P'],
		EffectType.DEBUFF),
	'-heat' : Effect('heat', 			['B', 'Q', 'X'],
		EffectType.DEBUFF),
	
	'invis' : Effect('invisibility', 	['L', 'V', 'X'],
		EffectType.BUFF)
}
	