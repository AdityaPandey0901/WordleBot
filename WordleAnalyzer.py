import numpy as np
import pandas as pd
import seaborn as sns

class WordleAnalyzer:

    def __init__(self,sim_name, solver_name,corpus):
        self.sim_name = sim_name
        self.solver_name = solver_name
        self.corpus = corpus

        self.result_df = self.runTest()

    
    def runTest(self):
        corpus_length = len(self.corpus)
        num_tries_array = np.zeros(corpus_length)

        Sim = self.sim_name('EMPTY')
        Solver = self.solver_name(self.corpus)

        for i,word in enumerate(self.corpus):
            Sim.reset(word)
            Solver.reset()

            while(Sim.win==False):
                Sim_Output=Sim.play(Solver.generate())
                Solver.update(Sim_Output[0])
            
            num_tries_array[i] = Sim.getTries()

        result_df = pd.DataFrame(index=self.corpus)
        result_df['num_tries'] = num_tries_array
        return result_df
    
    def getAnalysis(self):
        avg_tries = self.result_df.mean()
        print("Average tries : ",avg_tries)
        sns.histplot(self.result_df.num_tries.values)
    
    def getTriesGreater(self,limit, return_words=False):
        greater_than = self.result_df[self.result_df['num_tries'] > limit]

        count = greater_than.count().values[0]
        percent_count = count*100/len(self.result_df)

        output = [count, percent_count]
        if(return_words):
            output.append(greater_than)
        
        return output

    def getTriesLesser(self,limit, return_words=False):
        lesser_than = self.result_df[self.result_df['num_tries'] < limit]

        count = lesser_than.count().values[0]
        percent_count = count*100/len(self.result_df)

        output = [count, percent_count]
        if(return_words):
            output.append(lesser_than)
        
        return output
        
    def getInBetween(self,upper_limit, lower_limit, return_words=False):
        in_between = self.result_df[(self.result_df['num_tries'] < upper_limit) & (self.result_df['num_tries'] > lower_limit)]

        count = in_between.count().value[0]
        percent_count = count*100/len(self.result_df)

        output = [count, percent_count]
        if(return_words):
            output.append(in_between)
        
        return output

