import random
from time import time
from exact import Exact
from localSearch import LocalSearch


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

            t_start_exact = time()
            Aopt, Bopt, Fopt = exact.apply()
            t_stop_exact = time()
            t_start_ls = time()
            A1, B1, F1 = locSearch.apply()
            t_stop_ls = time()

            alltimes[0][i] = t_stop_exact - t_start_exact
            alltimes[1][i] = t_stop_ls - t_start_ls

            delta_alltimes[0][i] = 0
            delta_alltimes[1][i] = deltaF(F1, Fopt)
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


Rmax = 50
Itasks_max = 5
launch(Rmax, Itasks_max, True)
