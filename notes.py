#! /usr/bin/python3

"""SmallMusicPlayer

SmallMusicPlayer is available under the MIT License (MIT). See LICENSE.

Usage:
	SMP 
	SMP -f INPUTFILE -t OUTPUTFILE
	SMP -s INPUTSTR -t OUTPUTFILE

Options:
	-f INPUTFILE	The input file.
	-t OUTPUTFILE	The output file.
	-s INPUTFILE	From an input str.
	-p		Play the sound with vlc.
	-h		Show this help.
"""

import wave, math, random, os, time

from docopt import docopt

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

	def length(self):
		"""Returns the duration of the partition in seconds."""
		duration = float()
		for n in self:
			duration += n.tuple()[1]
		duration = float(duration/1000)
		return duration

	def save(self, filename='tmp.wav'):
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

	def play(self):
		sound_filename = 'tmp_{}.wav'.format(random.randint(0, 1000))
		self.save(filename=sound_filename)

		print("Running VLC.")

		os.system("vlc {0} && rm {0}".format(sound_filename))




class ParseError(Exception):
	pass

class Parser:
	def __init__(self, partition, input_str):
		self.partition = partition
		self.input_str = input_str

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
		current_duree = DUREE['noire']
		current_nuance = NUANCES['medium']

		instr = self.get_instr_list()
		for i in instr:
			if i in DUREE:
				current_duree = DUREE[i]
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
	print("Bytecode:\n" + str(Parser(part, 'Si2 Do3 Do3# --  forte croche Si Do2 - medium Re3 Do3# Do3').parse()))
	part.play()
	part.save()