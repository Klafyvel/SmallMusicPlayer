#! /usr/bin/python3

NOTES={
	"Do":131,
	"Do#":139,
	"Re":147,
	"Re#":156,
	"Mi":165,
	"Fa":175,
	"Fa#":185,
	"Sol":196,
	"Sol#":208,
	"La":220,
	"La#":233,
	"Si":247,
	"Do2":262,
	"Do2#":277,
	"Re2":294,
	"Re2#":311,
	"Mi2":330,
	"Fa2":349,
	"Fa2#":370,
	"Sol2":392,
	"Sol2#":415,
	"La2":440,
	"La2#":466,
	"Si2":494,
	"Silence":0,
}
#temps en millisecondes
DUREE={
	"croche":250,
	"noire":500,
	"blanche":1000,
}
NUANCES={
	"piano":0.3,
	"medium":0.6,
	"forte":1,
}

class Note:
	def __init__(self, note, duree, nuance=NUANCES["medium"]):
			self.note = note
			self.duree = duree
			self.nuance = nuance

	def __str__(self):
		return '({}, {}, {})'.format(self.note, self.duree, self.nuance)

	def tuple(self):
		return (self.note, self.duree, self.nuance)

silence = lambda duree: Note(NOTES["Silence"], duree)
SILENCES = {
	'-': silence(DUREE['croche']),
	'--': silence(DUREE['noire']),
	'---': silence(DUREE['blanche']),
}

class Partition(list):
	def __str__(self):
		s = str()
		for idx, n in enumerate(self):
			s += '{}:\t{}\n'.format(idx,n) 
		return s


class ParseError(Exception):
	pass

class Parser:
	def __init__(self, partition, input_str):
		self.partition = partition
		self.input_str = input_str
		self.current_note = silence

	def is_allowed_instr(self, word):
		if not word in NOTES and not word in DUREE and not word in NUANCES and not word in SILENCES:
			raise ParseError("'{}' is not an allowed word".format(word))
		return True

	def get_instr_list(self):
		instr_list = []
		current_word = ''
		for c in self.input_str:
			if (c == ' ' or c== '\n') and not current_word == '':
				self.is_allowed_instr(current_word)
				instr_list.append(current_word)
				current_word = ''
			elif c != ' ':
				current_word += c
		return instr_list


	def parse(self):
		return str(self.get_instr_list())

if __name__ == '__main__':
	part = Partition()
	print(Parser(part, 'Si Do2 Do2# --  forte croche Si Do2').parse())