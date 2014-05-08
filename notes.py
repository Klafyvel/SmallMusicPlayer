#! /usr/bin/python3

NOTES=[
	"Do",
	"Do#",
	"Re",
	"Re#",
	"Mi",
	"Fa",
	"Fa#",
	"Sol",
	"Sol#",
	"La",
	"La#",
	"Si",
	"Do2",
	"Do2#",
	"Re2",
	"Re2#",
	"Mi2",
	"Fa2",
	"Fa2#",
	"Sol2",
	"Sol2#",
	"La2",
	"La2#",
	"Si2",
	"Silence",
]
#temps en millisecondes
TEMPS={
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
		return '({} {} {})'.format(self.note, self.duree, self.nuance)

	def tuple(self)
		return (self.note, self.duree, self.nuance)

silence = lambda duree: Note(NOTES["Silence"], duree)