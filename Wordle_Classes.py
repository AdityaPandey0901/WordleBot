import pandas as pd
import numpy as np
from numpy import genfromtxt
import random
import seaborn as sns
from wordfreq import word_frequency as wf

Word_Bank_File_Name = 'words.csv'
Historical_File_Name = 'historical.txt'

#12000 word file stored as words_12k
words_12k=pd.read_csv('data/'+Word_Bank_File_Name)['words'].str.upper()

#8K word refined file
words_refine=open('data/words_refine.txt','r').read().split('\n')

#Historical Words stored as words_historicals
historicals_txt=open('data/'+Historical_File_Name,'r').readlines()[0]
words_historicals=pd.DataFrame(historicals_txt.split(" "),columns=['words'])['words'].str.upper()

def unique(list1):
  
    
    unique_list = []
  
    
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list
    


def getCharDistribution(word_list):
    Chars_List={}
    for word in words['words']:
        chars=unique([*word])
        for c in chars:
            if c not in Chars_List:
                Chars_List[c]=0
            Chars_List[c]+=1
    Sorted_Chars=dict(sorted(Chars_List.items(),key=lambda x:x[1],reverse=True))
    
    return Sorted_Chars
    

def getMaxFreq(word_corpus):
    
    Old=wf(word_corpus[0],'en')
    Word_Track=word_corpus[0]
    
    for word in word_corpus:
        New=max(wf(word,'en'),Old)
        if(New>Old):
            Word_Track=word
        
        Old=New
        
    return Word_Track


def sortDict(Dict):
    '''THis method sorts a dictionary by the descending order of
        its values'''
    
    Ret_Dict = {key: Dict[key] for key in sorted(Dict.keys(), key=Dict.__getitem__,reverse=True)}

    return Ret_Dict
    
########################################
#Wordle Sim

class WordleSim:
    
    ##Initializes the state 2D array, with [guess letter, state]
    ## 0: Not in Word
    ## 1: Yellow
    ## 2: Green
    ## 
    
    def __init__(self,word):
        self.source_word=word
        self.num_tries=0
        self.Game_State=[[]]
        self.win=False
        
        for i in range(0,4):
            self.Game_State.append(["",-1])
        

    def __str__(self, word):
        self.source_word=word.upper()
        self.num_tries=0
        
    def play(self,guess):
        Char_List=[*guess.upper()]
        
        print(len(Char_List))
        for i in range(0,len(Char_List)):
            state_var=0
            if Char_List[i]==[*self.source_word][i]:
                state_var=2
                
            elif Char_List[i] in [*self.source_word]:
                state_var=1
            
            self.Game_State[i]=[Char_List[i],state_var]
            
        self.num_tries+=1
        
        #################
        
        if self.source_word==guess:
            self.win=True
            
            
        return self.Game_State, self.num_tries, self.win
        
    def getTries(self):
        return self.num_tries


######################################
#Solver


class WordleSolver:




    def __init__(self, file_loc="data/words_refine.txt"):
        
        with open(file_loc,'r') as f:
            word_list = f.read().upper().split('\n')
        
        word_list.sort()
        self.word_list = word_list
        self.original_list=word_list
        self.correct_chars=[]
        self.notTieBreak=True
        
        self.randomizer="111000000000"
    
    
        #TieBreakVars
        self.used_chars=[]
        self.correct_chars=[]
        self.guesses=0
    
    
    
    
    def measure_distribution(self):
        dist_list = [{},{},{},{},{}]
        for i,word in enumerate(self.word_list):
            for j,letter in enumerate(word):
                dict = dist_list[j]
                if letter in dict:
                    dict[letter] = dict[letter]+1
                else:
                    dict[letter] = 1

        return dist_list
    
    def measure_frequency(self):
        letters = "".join(self.word_list)
        dict_freq = {}

        for i in range(60,91):
            dict_freq[chr(i)] = 0

        for i in letters:
            dict_freq[i] = dict_freq[i] + 1

        return dict_freq

    def generate_random(self):
        return random.choice(self.word_list)
    
    def generate_frequency(self):

        #Generates a word based on frequency ranker
        guess_word = ""
        max_score = 0
        dist_list = self.measure_frequency()

        for word in self.word_list:
            score = 0
            for j,letter in enumerate(word):
                score = score + dist_list[letter]
            
            if(score>max_score):
                max_score = score
                guess_word = word
        
        return guess_word

    def generate_frequency_wp(self):

        #Generates a word based on frequency ranker
        guess_word = ""
        max_score = 0
        dist_list = self.measure_frequency()

        for word in self.word_list:
            score = 0
            for j,letter in enumerate(word):
                if(letter not in word[:j]):
                    score = score + dist_list[letter]
            
            if(score>max_score):
                max_score = score
                guess_word = word
        
        return guess_word
    
    def generate_bucket(self):

        #Generates a word based on bucket ranker
        guess_word = ""
        max_score = 0
        dist_list = self.measure_distribution()

        for i,word in enumerate(self.word_list):
            score = 0
            for j,letter in enumerate(word):
                score = score + dist_list[j][letter]
            
            if(score>max_score):
                max_score = score
                guess_word = word
        
        return guess_word
    
    def generate_bucket_wp(self):

        #Generates a word based on bucket ranker with penalty
        guess_word = ""
        max_score = 0
        dist_list = self.measure_distribution()

        for i,word in enumerate(self.word_list):
            score = 0
            for j,letter in enumerate(word):
                if(letter not in word[:j]):
                    score = score + dist_list[j][letter]
            
            if(score>max_score):
                max_score = score
                guess_word = word
        
        return guess_word
    
################################################################

    def tieBreak(self):
        
        
        
        if(len(self.word_list)>2 and self.guesses>4):
            return ''
    
        
        #List of remaining letters
        Letters=self.getRemLetters()
        Letters,Ranks=self.rankRemLetters(Letters)
        
        
        #Now letters are sorted, lets get max score
        maxscore=0
        ret_word=''
        
        
        Word_Scores={}
        
            
            
            
        for word in self.original_list:
            score=0
            
            for L in Letters:
            
                if L in word:
                    
                    score+=1*Ranks[L]
            

            if score>2:
                Word_Scores[word]=score
                    
                
        Word_Scores=sortDict(Word_Scores)
        
        if(len(Word_Scores)>0):
            return list(Word_Scores.keys())[0]
        else:
            
            return ''
        
        
    def checkTie(self):
        
        guess_word = ""
        max_score = 0
        dist_list = self.measure_distribution()
        Score_Dict={}

        for i,word in enumerate(self.word_list):
            score = 0
            for j,letter in enumerate(word):
                score = score + dist_list[j][letter]
                
            
            Score_Dict[word]=score
        
        
        #print(np.std(list(Score_Dict.values())))
        if np.std(list(Score_Dict.values()))<=2 and len(Score_Dict)>0:
            
            return True
        
        else:
            return False
        
        

    def generate_mixed_wp(self):
        self.guesses+=1
        word1=self.generate_bucket_wp()
        word2=getMaxFreq(self.word_list)

        Path=self.randomizer[0]
        self.randomizer=self.randomizer[1:]
        

        if(Path=='1'):
            returner=word1
        else:
            returner=word2
        
        
        #TieBreak
        
        if(self.checkTie()==True):
            word3=self.tieBreak()

            
            #print(self.word_list)
            

            
            if(len(word3)>0):
                returner=word3
    

        #Update usechars
        
        for char in returner:
            
            if char in self.used_chars:
                x=0
                
            else:
                self.used_chars.append(char)
            
            
            

            
        return returner

    
    
    
    def rankRemLetters(self, Letters):
        
        Ranks={Letters[i]:0 for i in range(0,len(Letters))}
           
        
        for each in range(0,len(Letters)):
            
            for word in self.word_list:
                
                if(Letters[each] in word):
                    
                    Ranks[Letters[each]]+=1
        
        #Now to do a Descending Bubblesort on a dict
        
        Ranks=sortDict(Ranks)

        
                    
        return list(Ranks.keys()),Ranks
     
    
    
    
    def getRemLetters(self):
        
        #List of all chars, unprioritized
        
        RetList=[]
        
        
        for word in self.word_list:
            
            for char in word:
                
                occurences={}
                
                #Case 1: Double char but it has been guessed
                if char in self.correct_chars:
                    
                    #repeat checker
                    if char in occurences:
                        RetList.append(char)
                        
                    else:
                        occurences[char]=1
                
                elif (char in self.used_chars)==False:
                    
                    if (char in RetList)==False:
                        
                        RetList.append(char)  

        

        return RetList
                    




    def update(self, info=[]):
        new_word_list = []
        
        
        #Update correct_chars:
        if(len(info)>0):
            
            for char,value in info:
                if value==2:
                    if char in self.correct_chars:
                        x=0
                    else:
                        self.correct_chars.append(char)
        
        
        for i,word in enumerate(self.word_list):
            f = 0
            for j,value in enumerate(info):
                letter = value[0]
                letter_info = value[1]

                if(letter in word):
                    if(letter_info==0):
                        f=1
                        break
                    elif(letter_info==1 and word[j]==letter):
                        f=1
                        break
                    elif(letter_info==2 and word[j]!=letter):
                        f=1
                        
                        break
                    
                else:
                    if(letter_info>=1):
                        f=1
                        break
            if(f==0):
                new_word_list.append(word)
                
                
        self.word_list = new_word_list
    
    def len_list(self):
        return len(self.word_list)
    
    def return_list(self):

        ret_list=self.word_list.copy()
        random.shuffle(ret_list)
        return ret_list

    def reset(self, file_loc="data/words.txt"):
        with open(file_loc,'r') as f:
            word_list = f.read().upper().split('\n')

        word_list.sort()
        self.word_list = word_list


