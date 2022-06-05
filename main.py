# python native
from sys import argv
# custom libraries
from launcher import Launcher


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
    launcher = Launcher(params)
    if 'task_size' in params:
        m, n = params['task_size'].split(',')
        L, T = launcher.generate_task(int(m), int(n))
        launcher.individual(L, T, params['log'] == '1', params['exact'],
                   params['local'], params['genetic'])
    elif 'task_file' in params:
        try:
            L, T = launcher.generate_task_from_file(params['task_file'])
            launcher.individual(
                L, T, params['log'] == '1', params['exact'], params['local'], params['genetic'])
        except Exception as e:
            print(e)
    elif 'r_max' in params and 'i_tasks' in params:
        launcher.experiment(int(params['r_max']), int(params['i_tasks']), params['log'] ==
                   '1',  params['exact'], params['local'], params['genetic'], params['plots'])
