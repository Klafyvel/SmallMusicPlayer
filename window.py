#! /usr/bin/python3

"""
SmallMusicPlayer is available under the MIT License. See LICENSE.
"""
from tkinter import *
from notes import Partition, Parser, ParseError

class MainWindow(Frame):
	def __init__(self, window, parser=None, **kwargs):
		Frame.__init__(self, window, width=800, height=600, **kwargs)
		self.pack(fill=BOTH)

		self.window = window

		self.parser = parser
		self.input_str = ''
		self.output_file = ''

		self.create_widgets()

	def create_widgets(self):

		# Menu
		self.menu_bar = Menu(self.window)

		self.file = Menu(self.menu_bar, tearoff=0)
		self.menu_bar.add_cascade(label='File', underline=0, menu=self.file)

		self.file.add_command(label='Open File', underline=0, command=self.open)
		self.file.add_command(label='Close File', underline=0, command=self.close)
		self.file.add_separator()
		self.file.add_command(label="Quit", underline=0, command=self.quit)

		self.window.config(menu=self.menu_bar)

		# Debug display
		self.out_frame= LabelFrame(self, width=800, height=100, borderwidth=1, text='Parser messages')
		self.out_frame.pack(side='bottom', fill=BOTH)
		self.out = Text(self.out_frame, height=10)
		self.out.config(bg='black', fg='orange', state=DISABLED)
		self.out.pack(fill=BOTH)

		#Code display
		self.edit_frame = LabelFrame(self, width=300, height=300, borderwidth=1, text='Notes')
		self.edit_frame.pack(side='left', fill=Y)
		self.edit = Text(self.edit_frame)
		self.edit.pack()

		#options
		self.options_frame = LabelFrame(self, width=100, height=400, borderwidth=1, text='Options')
		self.options_frame.pack(side="top", fill=X)

		self.var_output_file = StringVar()
		self.lbl_output_location = Label(self.options_frame,text='Output file name:' )
		self.lbl_output_location.pack()
		self.output_location = Entry(self.options_frame, textvariable=self.var_output_file, width =20)
		self.output_location.pack()
		self.output_location.delete(0, END)
		self.output_location.insert(0, "name")

		self.var_create_output_file = IntVar()
		self.var_play_sound_with_vlc = IntVar()

		self.case_output_file = Checkbutton(self.options_frame, text='Write output in a file', variable=self.var_create_output_file)
		self.case_output_file.pack()
		self.case_play_sound = Checkbutton(self.options_frame, text='Play generated sound with vlc', variable=self.var_play_sound_with_vlc)
		self.case_play_sound.pack()

		self.btn_run = Button(self.options_frame, text='Compile', command=self.run)
		self.btn_run.pack()

	def load_input_str(self):
		self.input_str = self.edit.get(1.0, END)
	def parser_print(self, output_str):
		self.out.config(state=NORMAL)
		self.out.insert(INSERT, output_str + '\n')
		self.out.config(state=DISABLED)
	def open(self):
		pass
	def close(self):
		pass
	def run(self):
		part = Partition()
		self.load_input_str()
		self.parser_print('Begin parsing...')
		try:
			Parser(part, str(self.input_str)).parse()
		except ParseError as e:
			self.parser_print(str(e))
			return
		else:
			self.parser_print('Parsed !')

			if self.var_create_output_file.get() == 1:
				self.parser_print('Writing output...')
				part.save(filename=self.var_output_file.get())
			if self.var_play_sound_with_vlc.get() == 1:
				self.parser_print('Playing output...')
				part.play()
			self.parser_print('Done')


if __name__ == '__main__':
	f = Tk()
	m = MainWindow(f)

	m.mainloop()
	m.destroy()