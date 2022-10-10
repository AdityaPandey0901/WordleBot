from WordleSolver import WordleSolver
import random

class RandomSolver(WordleSolver):
    def generate(self):
        return random.choice(self.word_list)