import random
import matplotlib.pyplot as plt
from time import time
from sys import argv
import os
from exact import Exact
from localSearch import LocalSearch
from genetic import Genetic
from pandas import read_excel


def experiment(R, Itasks, log=False, run_exact=False, run_local=False, run_genetic=False, plots=False):
    times = [[] for _ in range(3)]
    deltas = [[] for _ in range(3)]
    k_range = range(4, R+1, 1)
    for k in k_range:
        alltimes = [[0]*Itasks for _ in range(3)]
        delta_alltimes = [[0]*Itasks for _ in range(3)]
        for i in range(0, Itasks):
            L, T = generate_task(k, 10*k)

            if run_exact:
                exact = Exact(L, T, log)
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

    print('\n\n*** Results ***')
    print('\n** Average Time **')
    if run_exact:
        print(f'Exact algorithm:\n {times[0]}')
    if run_local:
        print(f'Local search algorithm:\n {times[1]}')
    if run_genetic:
        print(f'Genetic algorithm:\n {times[2]}\n')
    if run_local or run_genetic:
        print('\n** Average Delta **')
        if run_local:
            print(f'Local search algorithm:\n {deltas[1]}')
        if genetic:
            print(f'Genetic algorithm:\n {deltas[2]}')

    if(plots):

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
        plt.plot(k_range, deltas[2], color='#B7E5DD',
                 label='Genetic Algorithm')
        plt.title("Relation of dimension to average delta")
        plt.legend()
        plt.ylabel('Average Delta')
        plt.xlabel('Task Dimension k, m=k, n=10*k')
        plt.show()


def individual(L, T, log=False, run_exact=False, run_local=False, run_genetic=False):
    print(f'\nm={len(L[0])}, n={len(L)}\n')
    for row in T:
        print(*row, sep=' ')
    Aopt, Bopt, Fopt, A1, B1, F1, A2, B2, F2 = None, None, None, None, None, None, None, None, None
    if run_exact:
        exact = Exact(L, T, log)
        Aopt, Bopt, Fopt = exact.apply()
    if run_local:
        locSearch = LocalSearch(L, T, log)
        A1, B1, F1 = locSearch.apply()
    if run_genetic:
        genetic = Genetic(L, T, log)
        A2, B2, F2 = genetic.apply()

    print('\n\n*** Results ***')
    if run_exact:
        print(f'Exact algorithm: A={Aopt}, B={Bopt}, F={Fopt}')
    if run_local:
        print(f'Local Search algorithm: A={A1}, B={B1}, F={F1}')
    if run_genetic:
        print(f'Genetic algorithm: A={A2}, B={B2}, F={F2}')


def generate_task_from_file(path):
    print(f'\nReading file: {path}')
    if os.path.exists(path):
        file = read_excel(path, index_col=0, header=None)
        print('\nParsed task:')
        print(file)
        n, m = file.shape
        L = [f'Lang#{i+1}' for i in range(m+1)]
        T = []
        for row in file.itertuples():
            T.append([row[cel] for cel in row])
        return L, T
    else:
        raise Exception('Cannot localte given file or the file does not exist')


def generate_task(m, n):
    T = []
    L = [f'Lang#{i+1}' for i in range(0, m)]
    for _ in range(0, n):
        T.append([random.randint(0, 1) for _ in range(0, m)])
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
    params = {'log': 0, 'exact': False,
              'genetic': False, 'local': False, 'plots': False}
    for p in argv[1:]:
        key = p.split('=')[0] if '=' in p else p
        value = p.split('=')[1] if '=' in p else True
        params[key] = value
        print(f'Setting param {key} to {value}')
    if 'task_size' in params:
        m, n = params['task_size'].split(',')
        L, T = generate_task(int(m), int(n))
        individual(L, T, params['log'] == '1', params['exact'],
                   params['local'], params['genetic'])
    elif 'task_file' in params:
        try:
            L, T = generate_task_from_file(params['task_file'])
            individual(
                L, T, params['log'] == '1', params['exact'], params['local'], params['genetic'])
        except Exception as e:
            print(e)
    elif 'r_max' in params and 'i_tasks' in params:
        experiment(int(params['r_max']), int(params['i_tasks']), params['log'] ==
                   '1',  params['exact'], params['local'], params['genetic'], params['plots'])
