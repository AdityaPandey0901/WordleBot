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
       
        for i in range(0,len(Char_List)):
            state_var=0
            if Char_List[i]==[*self.source_word][i]:
                state_var=2
               
            elif Char_List[i] in [*self.source_word]:
                state_var=1
           
            self.Game_State[i]=[Char_List[i],state_var]
           
        self.num_tries+=1
       
        #################
       
        win_Counter=0
        for i in range(0,5):
            win_Counter+=self.Game_State[i][1]
       
        if win_Counter==10:
            self.win=True
           
           
        return self.Game_State, self.num_tries, self.win
       
    def getTries(self):
        return self.num_tries