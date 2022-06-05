import random
from time import time
from sys import argv
from exact import Exact
from localSearch import LocalSearch
from genetic import Genetic


# add argv to read file name, R, Itasks, log

def launch(R, Itasks, log=False):
    times = [[0]*R for _ in range(3)]
    deltas = [[0]*R for _ in range(3)]
    for k in range(4, R+1):
        alltimes = [[0]*Itasks for _ in range(3)]
        delta_alltimes = [[0]*Itasks for _ in range(3)]
        for i in range(0, Itasks):
            L, T = generate_task(k)

            exact = Exact(L, T, log=False)
            locSearch = LocalSearch(L, T, log)
            genetic = Genetic(L, T, log)

            t_start_exact = time()
            Aopt, Bopt, Fopt = exact.apply()
            t_stop_exact = time()
            # t_start_ls = time()
            # A1, B1, F1 = locSearch.apply()
            # t_stop_ls = time()
            t_start_genetic = time()
            A2, B2, F2 = genetic.apply()
            t_stop_genetic = time()

            alltimes[0][i] = t_stop_exact - t_start_exact
            # alltimes[1][i] = t_stop_ls - t_start_ls
            alltimes[2][i] = t_stop_genetic - t_start_genetic

            delta_alltimes[0][i] = 0
            # delta_alltimes[1][i] = deltaF(F1, Fopt)
            delta_alltimes[2][i] = deltaF(F2, Fopt)
        times[0][k-1], times[1][k-1], times[2][k-1] = average(
            alltimes[0]), average(alltimes[1]), average(alltimes[2])
        deltas[0][k-1], deltas[1][k-1], deltas[2][k-1] = average(
            delta_alltimes[0]), average(delta_alltimes[1]), average(delta_alltimes[2])
    print(times[0])
    print(times[1])
    print(times[2])
    print('Deltas:')
    print(deltas[1])
    print(deltas[2])


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
    print('+  task_file - relative path of .xlsx file with problem description, \ncan be used only separately from r_max, i_tasks')
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

    launch(int(params['r_max']), int(params['i_tasks']), params['log'] == '1')
