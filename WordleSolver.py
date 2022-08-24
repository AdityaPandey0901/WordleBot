import random
class WordleSolver:


    def __init__(self, file_loc="data/words.txt"):
        with open(file_loc,'r') as f:
            word_list = f.read().upper().split('\n')

        word_list.sort()
        self.word_list = word_list
    
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

    def generate_random(self):
        return random.choice(self.word_list)
    
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


    def update(self, info=[]):
        new_word_list = []
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
        return self.word_list


