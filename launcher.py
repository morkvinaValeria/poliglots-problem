# python native
import os
import random
from time import time
# python libraries
import matplotlib.pyplot as plt
from pandas import read_excel
# custom libraries
from exact import Exact
from localSearch import LocalSearch
from genetic import Genetic


class Launcher:
    
    def __init__(self, params):
        self.params = params
        self.log = params['log'] == 1
        self.plots = params['plots']
        self.run_exact = params['exact']
        self.run_genetic = params['genetic']
        self.run_local = params['local'] 
        self.i_tasks = params['i_tasks']

    def experiment(self):
        R = self.params['r_max']
        Itasks = self.params['i_tasks']
        times = [[] for _ in range(3)]
        deltas = [[] for _ in range(3)]
        k_range = range(4, R+1, 5)
        for k in k_range:
            alltimes = [[0]*Itasks for _ in range(3)]
            delta_alltimes = [[0]*Itasks for _ in range(3)]
            for i in range(0, Itasks):
                L, T = self.generate_task(k, 10*k)

                if self.run_exact:
                    exact = Exact(L, T, self.log)
                    t_start_exact = time()
                    Aopt, Bopt, Fopt = exact.apply()
                    t_stop_exact = time()
                    alltimes[0][i] = t_stop_exact - t_start_exact
                    delta_alltimes[0][i] = 0
                if self.run_local:
                    locSearch = LocalSearch(L, T, self.log)
                    t_start_ls = time()
                    A1, B1, F1 = locSearch.apply()
                    t_stop_ls = time()
                    alltimes[1][i] = t_stop_ls - t_start_ls
                    delta_alltimes[1][i] = self.deltaF(F1, Fopt)
                if self.run_genetic:
                    genetic = Genetic(L, T, self.log)
                    t_start_genetic = time()
                    A2, B2, F2 = genetic.apply()
                    t_stop_genetic = time()
                    alltimes[2][i] = t_stop_genetic - t_start_genetic
                    delta_alltimes[2][i] = self.deltaF(F2, Fopt)

            times[0].append(self.average(alltimes[0]))
            times[1].append(self.average(alltimes[1]))
            times[2].append(self.average(alltimes[2]))
            deltas[0].append(self.average(delta_alltimes[0]))
            deltas[1].append(self.average(delta_alltimes[1]))
            deltas[2].append(self.average(delta_alltimes[2]))

        print('\n\n*** Results ***')
        print('\n** Average Time **')
        if self.run_exact:
            print(f'Exact algorithm:\n {times[0]}')
        if self.run_local:
            print(f'Local search algorithm:\n {times[1]}')
        if self.run_genetic:
            print(f'Genetic algorithm:\n {times[2]}\n')
        if self.run_local or self.run_genetic:
            print('\n** Average Delta **')
            if self.run_local:
                print(f'Local search algorithm:\n {deltas[1]}')
            if genetic:
                print(f'Genetic algorithm:\n {deltas[2]}')

        if(self.plots): self.show_plots(k_range, times, deltas)
    
        print('\n\n*** Results ***')
        if self.run_exact:
            print(f'Exact algorithm: A={Aopt}, B={Bopt}, F={Fopt}')
        if self.run_local:
            print(f'Local Search algorithm: A={A1}, B={B1}, F={F1}')
        if self.run_genetic:
            print(f'Genetic algorithm: A={A2}, B={B2}, F={F2}')
            

    def show_plots(self, k_range, times, deltas):
        plt.figure(1)
        plt.plot(k_range, times[0], color='#F1F0C0', label='Exact Algorithm')
        plt.plot(k_range, times[1], color='#B1BCE6', label='Local Search')
        plt.plot(k_range, times[2], color='#B7E5DD', label='Genetic Algorithm')
        plt.title("Relation of dimension to average time ")
        plt.legend()
        plt.ylabel('Average Time')
        plt.xlabel('Task Dimension k, m=k, n=10*k')
        plt.figure(2)
        plt.plot(k_range, deltas[0], color='#F1F0C0', label='Exact Algorithm')
        plt.plot(k_range, deltas[1], color='#B1BCE6', label='Local Search')
        plt.plot(k_range, deltas[2], color='#B7E5DD', label='Genetic Algorithm')
        plt.title("Relation of dimension to average delta")
        plt.legend()
        plt.ylabel('Average Delta')
        plt.xlabel('Task Dimension k, m=k, n=10*k')
        plt.show()


    def individual(self, L, T):
        print(f'\nm={len(L[0])}, n={len(L)}\n')
        for row in T:
            print(*row, sep=' ')
        Aopt, Bopt, Fopt, A1, B1, F1, A2, B2, F2 = None, None, None, None, None, None, None, None, None
        if self.run_exact:
            exact = Exact(L, T, self.log)
            Aopt, Bopt, Fopt = exact.apply()
        if self.run_local:
            locSearch = LocalSearch(L, T, self.log)
            A1, B1, F1 = locSearch.apply()
        if self.run_genetic:
            genetic = Genetic(L, T, self.log)
            A2, B2, F2 = genetic.apply()
        

    def generate_task_from_file(self, path):
        print(f'\nReading file: {path}')
        if os.path.exists(path):
            file = read_excel(path, index_col=0, header=None)
            n, m = file.shape
            L = [f'Lang#{i+1}' for i in range(m+1)]
            T = []
            for row in file.itertuples():
                T.append([cel for cel in row])
            return L, T
        else:
            raise Exception('Cannot localte given file or the file does not exist')


    def generate_task(self, m, n):
        T = []
        L = [f'Lang#{i+1}' for i in range(0, m)]
        for _ in range(0, n):
            T.append([random.randint(0, 1) for _ in range(0, m)])
        return L, T


    def deltaF(self, f, fopt):
        return (f-fopt)


    def average(self, lst):
        return sum(lst) / len(lst)
