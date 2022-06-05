import random
from time import time
from sys import argv
import os
from exact import Exact
from localSearch import LocalSearch
from genetic import Genetic
from pandas import read_excel


# add argv to read file name, R, Itasks, log

def experiment(R, Itasks, log=False, run_exact=False, run_local=False, run_genetic=False):
    times = [[] for _ in range(3)]
    deltas = [[] for _ in range(3)]
    for k in range(4, R+1, 10):
        alltimes = [[0]*Itasks for _ in range(3)]
        delta_alltimes = [[0]*Itasks for _ in range(3)]
        for i in range(0, Itasks):
            L, T = generate_task(k)

            if run_exact: 
                exact = Exact(L, T, log=False)
                t_start_exact = time()
                Aopt, Bopt, Fopt = exact.apply()
                t_stop_exact = time()
                alltimes[0][i] = t_stop_exact - t_start_exact
                delta_alltimes[0][i] = 0
            if run_local: 
                locSearch = LocalSearch(L, T, log)
                t_start_ls = time()
                A1, B1, F1 = locSearch.apply()
                t_stop_ls = time()
                alltimes[1][i] = t_stop_ls - t_start_ls
                delta_alltimes[1][i] = deltaF(F1, Fopt)
            if run_genetic: 
                genetic = Genetic(L, T, log)
                t_start_genetic = time()
                A2, B2, F2 = genetic.apply()
                t_stop_genetic = time()
                alltimes[2][i] = t_stop_genetic - t_start_genetic
                delta_alltimes[2][i] = deltaF(F2, Fopt)
            
        times[0].append(average(alltimes[0]))
        times[1].append(average(alltimes[1]))
        times[2].append(average(alltimes[2]))
        deltas[0].append(average(delta_alltimes[0]))
        deltas[1].append(average(delta_alltimes[1]))
        deltas[2].append(average(delta_alltimes[2]))

    print(f'\nAverage time for exact algorithm:\n {times[0]}')
    print(f'Average time for local search algorithm:\n {times[1]}')
    print(f'Average time for genetic algorithm:\n {times[2]}\n')
    print(f'Average delta for local search algorithm:\n {deltas[1]}')
    print(f'Average delta for genetic algorithm:\n {deltas[2]}')


def individual(k, log=False):
    L, T = generate_task(k)
    exact = Exact(L, T, log=False)
    locSearch = LocalSearch(L, T, log)
    genetic = Genetic(L, T, log)
    Aopt, Bopt, Fopt = exact.apply()
    print(f'\nExact algorithm: A={Aopt}, B={Bopt}, F={Fopt}\n')
    A1, B1, F1 = locSearch.apply()
    print(f'Local Search algorithm: A={A1}, B={B1}, F={F1}\n')
    A2, B2, F2 = genetic.apply()
    print(f'Genetic algorithm: A={A2}, B={B2}, F={F2}\n')


def individual_from_file(path, log=False, run_exact=False, run_local=False, run_genetic=False):
    print(f'\nReading file: {path}')
    if os.path.exists(path):
        file = read_excel(path, index_col=0, header=None)
        print('\nParsed task:')
        print(file)
        n,m = file.shape
        L = [f'Lang#{i+1}' for i in range(m+1)]
        T = []
        for row in file.itertuples():
            T.append([row[cel] for cel in row])
    else:
        print('Cannot localte given file or the file does not exist')


def generate_task(k):
    T = []
    L = [f'Lang#{i+1}' for i in range(0, k)]
    for _ in range(0, 10*k):
        T.append([random.randint(0, 1) for _ in range(0, k)])
    return L, T


def deltaF(f, fopt):
    return (f-fopt)


def average(lst):
    return sum(lst) / len(lst)
    


if argv[1] == 'help':
    print('Poliglots problem CLI manual')
    print('-------------------------------------------------------------------')
    print('Values for the following arguments is assigned with \'=\' character')
    print('+  r_max     - max problem size (for statistical experiments)')
    print('+  i_tasks   - quantity of random tasks of each problem size (for statistical experiments)')
    print('+  task_size - launches one demonstrative task of geiven problem size (pass m,n e.g. 100,10)')
    print('+  task_file - relative path of .xlsx file with problem description in form of matrix T, \ncan be used only separately from r_max, i_tasks')
    print('+  log       - 0 or 1 disables or enables logs, 0 by default')
    print('-------------------------------------------------------------------')
    print('The follwing arguments are flags, they are passed without values')
    print('+  exact   - launches exact algorithm (exaustive search)')
    print('+  genetic - launches genetic algorithm')
    print('+  local   - launches local search algorithm')
    print('+  plots   - show launch results comparison plots')
else:
    params = {'log': 0}
    for p in argv[1:]:
        key = p.split('=')[0]
        value = p.split('=')[1]
        params[key] = value
        print(f'Setting param {key} to {value}')
    if 'task_size' in params:
        individual(int(params['task_size']), params['log'] == '1')
    elif 'task_file' in params: 
        individual_from_file(params['task_file'], params['log'] == '1')
    elif 'r_max' in params and 'i_tasks' in params:
        experiment(int(params['r_max']), int(
            params['i_tasks']), params['log'] == '1')
