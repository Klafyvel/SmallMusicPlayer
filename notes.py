#! /usr/bin/python3

"""SmallMusicPlayer

SmallMusicPlayer is available under the MIT License. See LICENSE.

Usage: 
	SMP -f INPUTFILE (-t OUTPUTFILE | -p)
	SMP -s INPUTSTR (-t OUTPUTFILE | -p)
"""

import wave, math, random, os, time

from docopt import docopt

# Notes with Hz values
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
	"Do3":523,
	"Do3#":554,
	"Re3":587,
	"Re3#":622,
	"Mi3":659,
	"Fa3":698,
	"Fa3#":740,
	"Sol3":784,
	"Sol3#":830,
	"La3":880,
	"La3#":932,
	"Si3":988,
	"Silence":0,
}
DUREE={
	"croche":500,
	"noire":1000,
	"blanche":2000,
}

NUANCES={
	"piano":0.15,
	"medium":0.3,
	"forte":0.6,
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
	'-': lambda :silence(DUREE['croche']),
	'--': lambda:silence(DUREE['noire']),
	'---': lambda:silence(DUREE['blanche']),
}

OTHER_OP = {
	"bpmSet": lambda parser, val: Parser.set_bpm(parser, val),
}


class Partition(list):
	saved_file = ''
	def __str__(self):
		s = str()
		for idx, n in enumerate(self):
			s += '{}:\t{}\n'.format(idx,n) 
		return s

	def length(self):
		"""Returns the duration of the partition in seconds."""
		duration = float()
		for n in self:
			duration += n.tuple()[1]
		duration = float(duration)/1000.0
		return duration

	def save(self, filename='tmp.wav'):
		self.saved_file = ''
		sound = wave.open(filename, 'w')
		canal_nb = 1
		octet_nb = 1
		fech = 44100
		ech_nb = int(self.length() * fech)
		params = (canal_nb, octet_nb, fech, ech_nb, 'NONE', 'not compressed')
		sound.setparams(params)

		for n in self:
			t = n.tuple()
			amplitude = 127.5*t[2]
			n_dur = int(float(t[1])/1000 *fech)
			for i in range(0, n_dur):
				val = wave.struct.pack('B', int(128 + amplitude*math.sin(2.0*math.pi*t[0]*i/fech)))
				sound.writeframes(val)
		sound.close()
		self.saved_file = filename

	def play(self):
		if self.saved_file is '':
			sound_filename = 'tmp_{}.wav'.format(random.randint(0, 1000))
			print('Creating temporary file: {}'.format(sound_filename))
			self.save(filename=sound_filename)
			self.saved_file = ''
		else:
			sound_filename = self.saved_file

		print("Running VLC.")
		if self.saved_file is '':
			order ="vlc {0} && rm -vf {0}".format(sound_filename)
			os.system(order)
		else:
			os.system("vlc {}".format(sound_filename))

class ParseError(Exception):
	pass

class Parser:
	def __init__(self, partition, input_str):
		self.partition = partition
		self.input_str = input_str
		self.bpm = 180
		self.current_line = 1

	def set_bpm(self, val):
		self.bpm = int(val)

	def is_allowed_instr(self, word):
		allowed = False
		allowed = allowed or word in NOTES 
		allowed = allowed or word in DUREE 
		allowed = allowed or word in NUANCES 
		allowed = allowed or word in SILENCES
		allowed = allowed or word in OTHER_OP
		try:
			allowed = allowed or isinstance(int(word), int)
		except ValueError:
			pass
		if not allowed:
			raise ParseError("'{}' is not an allowed word at line {}".format(word, self.current_line))
		return True

	def get_instr_list(self):
		instr_list = []
		current_word = ''
		for c in self.input_str:
			if (c == ' ' or c== '\n') and not current_word == '':
				self.is_allowed_instr(current_word)
				instr_list.append(current_word)
				current_word = ''
				self.current_line += 1
			elif c != ' ':
				current_word += c
		if not current_word == '': 
			self.is_allowed_instr(current_word)
			instr_list.append(current_word)
		return instr_list


	def parse(self):
		current_duree = int(DUREE['noire']/(self.bpm/60))
		current_nuance = NUANCES['medium']

		instr = self.get_instr_list()
		operating_arg = False
		operation = ''

		self.partition.saved_file = ''

		for i in instr:
			if operating_arg:
				OTHER_OP[operation](self, i)
				operation = ''
				operating_arg = False
			elif i in OTHER_OP:
				operating_arg = True
				operation = i
			elif i in DUREE:
				current_duree = int(DUREE[i]/(self.bpm/60))
			elif i in NUANCES:
				current_nuance = NUANCES[i]
			elif i in SILENCES:
				self.partition.append(silence(current_duree))
			elif i in NOTES:
				self.partition.append(Note(NOTES[i], current_duree, current_nuance))

		return self.partition

if __name__ == '__main__':
	args = docopt(__doc__)

	part = Partition()
	input_str = ""

	if args['-f']:
		with open(args['INPUTFILE'], 'r') as in_file:
			input_str = in_file.read()
	elif args['-s']:
		input_str = args['INPUTSTR']

	Parser(part, input_str).parse()

	if args['-t']:
		part.save(filename=args['OUTPUTFILE'])
	elif args['-p']:
		part.play()