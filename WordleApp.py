import kivy

kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from matplotlib import pyplot as plt
from kivy.uix.togglebutton import ToggleButton

import Wordle_Classes as Wrdle
from kivy.properties import ListProperty
import pandas as pd
import numpy as np
from numpy import genfromtxt
import random
import seaborn as sns
from wordfreq import word_frequency as wf
import pandas as pd
import threading
from kivy.clock import Clock


import time
import random
from kivy.config import Config


class WordleApp(App):
	Word_Bank_File_Name = 'words.csv'
	Historical_File_Name = 'historical.txt'
	words_12k=pd.read_csv('data/'+Word_Bank_File_Name)['words'].str.upper()


	historicals_txt=open('data/'+Historical_File_Name,'r').readlines()[0]
	corpus=pd.DataFrame(historicals_txt.split(" "),columns=['words'])['words'].str.upper()
	random.shuffle(corpus)
	index=0
	guesses=[]
	used=[]
	GTrack=[]
	total=0

	winFlag=True





	def startAGame(self,x):
		self.a.children[3].text="Round: "+str(self.total)+"\n"+'Started'
		self.a.children[3].bold=True
		self.guesses=[]
		
		self.winFlag=False
		Grey=np.array([88,88,88,256])/256
		#resets the board
		self.grid.clear_widgets()
		for i in range(30):
			self.grid.add_widget(Button(text=' '))


		guesses=[]
		if(self.index<len(self.corpus)):
			first=self.corpus[self.index]
			self.index+=1
			self.Sim=Wrdle.WordleSim(first) #Starts with random word
			self.Solver=Wrdle.WordleSolver()
			self.used.append(first)
		else:
			self.corpus=self.words_12k


	def on_enter(self, value):
		guess=self.input.text

		if(len(guess)==5 and self.winFlag==False):
			self.update(guess)

	def BotPlay(self,x=0):

		if(self.winFlag==False):
			guess=self.Solver.generate_mixed_wp()
			self.update(guess)
		else:
			self.startAGame(1)

	def checkWin(self,State):
		for each in State:
			if each[1]!=2:
				return False


		self.winFlag=True

		return True


	def recAuto(self,x):

		
		if(self.Auto.state=='down'):

			self.BotPlay()

		else:

			return False

		



	def AutoPlay(self,press):

		event=Clock.schedule_interval(self.recAuto, 1)




	def update(self,guess,x=0):

		if(not self.winFlag):
			
			self.guesses.append(guess.upper())
			State=self.Sim.play(guess)[0]
			self.Solver.update(State)    #Keep Solver up to date

			

			guess_no=len(self.guesses)
			Elements=self.grid.children
			
			#Colors
			Grey=np.array([88,88,88,256])/256
			Orange=(np.array([255,153,0,256])/256)
			Green=(np.array([51,153,51,256])/256)


			#Fills Grid Cells and Colors

			for i in range(0,len(Elements)):

				if (i<len(self.guesses)*5): #Fill in Guesses
					This_char=[*self.guesses[int(i/5)]][i%5]
					Elements[29-i].text=This_char

					State=self.Sim.play(self.guesses[int(i/5)])[0]

					if(State[i%5][1]==1):
						#Elements[29-i].background_normal=''
						Elements[29-i].background_color=Orange/Grey


					elif(State[i%5][1]==2):
						#Elements[29-i].background_normal=''
						Elements[29-i].background_color=Green/Grey
					Elements[29-i].line_color= Grey


			#Fill in recommended words
			temp=self.Solver.return_list()

			self.RecBox.text='\nSuggested Words:'

			for i in range(0,min(len(temp),10)):
				self.RecBox.text+='\n'+str(i+1)+': '+temp[i]



			

			

			#Check for Win Condition and populate others
			if(self.checkWin(State)):

				self.a.children[3].text="Round "+str(self.total)+"\n"+'Victory :)'
				self.total+=1
				self.GTrack.append(len(self.guesses))
				self.a.children[1].text="Avg Guesses: "+str(np.round(np.mean(self.GTrack),decimals=2))
				self.a.children[2].text="Success: "+str(np.round(len(self.GTrack)*100/self.total))+"%"
				

			elif(len(self.guesses)==6):
				self.total+=1
				self.a.children[3].text="Round: "+str(self.total)+"\n"+'Defeat :('

			






	def build(self):


		self.big=BoxLayout(orientation='horizontal')
		self.grid=GridLayout(cols=5,size_hint=(2,1),padding="12dp")
		self.buttons=BoxLayout(orientation='vertical')
		self.a=BoxLayout(orientation='vertical',size_hint=(0.15,1))
		
		self.a.add_widget(Label(text=' ',size_hint=(1,.15),pos_hint={'x':1,'y':1},halign="left"))
		self.a.add_widget(Label(text=' ',size_hint=(1,.15),pos_hint={'x':1,'y':.75},halign="left"))
		self.a.add_widget(Label(text=' ',size_hint=(1,.15),pos_hint={'x':1,'y':.75},halign="left"))
		self.a.add_widget(Label(text=' ',size_hint=(1,.55),pos_hint={'x':1,'y':.5},halign="left"))


		self.buttons.add_widget(Label(text='         ',size_hint=(.5, .02)))
		
		self.buttons.add_widget(Label(text='         ',size_hint=(.5, .15)))
		self.buttons.add_widget(Button(text = "Start Game",on_press = self.startAGame,size_hint=(.5, .2),pos_hint={'x':.5,'y':.6}))
		self.buttons.add_widget(Label(text='         ',size_hint=(.5, .15)))
		self.buttons.add_widget(Button(text = "Use Bot Guess",on_press = self.BotPlay,size_hint=(.5, .2),pos_hint={'x':.5,'y':.6}))
		self.buttons.add_widget(Label(text='',size_hint=(.5, .15)))
		self.Auto=ToggleButton(text='AutoPlay',size_hint=(.5,.2),pos_hint={"x":.5, "y":.6},on_press=self.AutoPlay)
		self.buttons.add_widget(self.Auto)
		self.buttons.add_widget(Label(text='',size_hint=(.5, .15)))
		self.input=TextInput(text='Your Guess', multiline=False,size_hint=(.5, .2),pos_hint={'x':.5,'y':1})
		
		

		self.input.bind(on_text_validate=self.on_enter)
		self.buttons.add_widget(self.input)
		self.buttons.add_widget(Label(text=' ',size_hint=(.5, .8)))

		#RecsBox

		self.RecBox=Label(text='\nSuggested Words:',size_hint=(1,.55),pos_hint={'x':.25,'y':1}, underline=False,valign="top")

		self.buttons.add_widget(self.RecBox)

		b=BoxLayout(orientation='horizontal')
		b.add_widget(Label(text=' ',size_hint=(.5,1)))
		
		self.buttons.add_widget(b)
		self.buttons.add_widget(Label(text=' ',size_hint=(.5, .1)))



		for i in range(30):
			self.grid.add_widget(Button(text=' '))

		self.big.add_widget(self.grid)
		self.big.add_widget(Label(text=' ',size_hint=(0.05,1)))
		self.big.add_widget(self.a)
		self.buttons.add_widget(Label(text='               ',size_hint=(1,1.0)))
		self.white=Button(text=' ',size_hint=(0.01,1), pos_hint={'x':1,'y':0})
		self.white.background_normal=''
		self.big.add_widget(Label(text=' ',size_hint=(0.5,1)))
		self.big.add_widget(self.white)
		self.big.add_widget(self.buttons)
		self.big.add_widget(Label(text='               ',size_hint=(.2,1.0)))
		self.big.outline_color=[1,0,0,1]

		return self.big



if __name__=='__main__':

	WordleApp().run()


























