# Poliglots Problem🔎🧠

## Install dependencies

To install all depended packages in _requirements.txt_ use the following command:  
`pip install -r requirements.txt`

---

## Launch the project🔃

To lanch the project use use the following command:  
`python main.py [params]`

---

## CLI Params

To see all params, you can use help:  
`python main.py help`

### Values for the following arguments is assigned with `=` character

- `r_min`- min problem size, min = 4, 4 by default (for statistical experiments)
- `r_max` - max problem size (for statistical experiments), max = 4200
- `r_step` - step of problem sizes from r_min to r_max, 1 by default (for statisctical experiments)
- `i_tasks` - quantity of random tasks of each problem size (for statistical experiments)
- `n_ratio` - ratio of number of poliglots to number of languages, 10 by default, max = 10
- `task_size` - launches one demonstrative task of geiven problem size (pass m,n e.g. 100,10)
- `task_file` - relative path of .xlsx file with problem description in form of matrix T, \ncan be used only separately from r_max, i_tasks'
- `log` - 0 or 1 disables or enables logs, 0 by default

### "Flag" arguments, they are passed without values

- `exact`- launches exact algorithm (exaustive search)
- `genetic` - launches genetic algorithm
- `local` - launches local search algorithm
- `plots` - show launch results comparison plots
