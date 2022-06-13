# python native
from sys import argv
# custom libraries
from launcher import Launcher


if argv[1] == 'help':
    print('Poliglots problem CLI manual')
    print('-------------------------------------------------------------------')
    print('Values for the following arguments is assigned with \'=\' character')
    print('+  r_min     - min problem size, min = 4, 4 by default (for statistical experiments)')
    print('+  r_max     - max problem size (for statistical experiments), max = 4200')
    print('+  r_step    - step of problem sizes from r_min to r_max, 1 by default (for statisctical experiments)')
    print('+  i_tasks   - quantity of random tasks of each problem size (for statistical experiments)')
    print('+  n_ratio   - ratio of number of poliglots to number of languages, 10 by default, max = 10')
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
              'genetic': False, 'local': False, 'plots': False, 'r_min': 4, 'r_interval': 1, 'n_ratio': 10}
    for p in argv[1:]:
        key = p.split('=')[0] if '=' in p else p
        value = p.split('=')[1] if '=' in p else True
        params[key] = value
        print(f'Setting param {key} to {value}')
    launcher = Launcher(params)
    print('\n')
    if 'n_ratio' in params or 'r_max' in params or 'r_min' in params:
        if int(params['n_ratio']) > 10 or int(params['r_max']) > 4200 or int(params['r_min']) < 4 or int(params['r_min']) > int(params['r_max']):
            print('Enter valid command, please see help')
    elif 'task_size' in params:
        m, n = params['task_size'].split(',')
        L, T = launcher.generate_task(int(m), int(n))
        launcher.individual(L, T)
    elif 'task_file' in params:
        try:
            L, T = launcher.generate_task_from_file(params['task_file'])
            launcher.individual(L, T)
        except Exception as e:
            print(e)
    elif 'r_max' in params and 'i_tasks' in params:
        launcher.experiment()
    else:
        print('Enter valid command, please see help')
