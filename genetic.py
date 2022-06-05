from cmath import inf
from copy import copy
import random


class Genetic:
    def __init__(self, L, T, log=False):
        self.L = L
        self.m = len(L)
        self.T = T
        self.Mu = int(self.m * 0.1) if int(self.m * 0.1) >= 3 else 3
        self.Lambda = self.Mu
        self.ws = self.Mu * 100
        self.H_max = self.m * 20
        self.H_maxconst = int(self.H_max * 0.1)
        self.log = log

    def apply(self):
        if(self.log):
            print('\n\n*** Genetic Algorithm ***\n')
        P = self.gen_pop_shot_gun()
        if self.log:
            print(f'Generated init population: \n{P}')
        best_pers = None
        best_score = inf
        h_count, h_const_count = 0, 0
        while h_count < self.H_max and h_const_count < self.H_maxconst:
            best_pers = P[0]
            ideal_calc = self.calc_ideal(best_pers)
            if ideal_calc[1]:
                if self.log:
                    print(f'Perfect case found')
                best_score = ideal_calc[0]
                break
            temp_best_score = ideal_calc[0]
            prop_pos = self.calc_prop_pos(P)
            if self.log:
                print(f'Proportional possibilities: \n{prop_pos}')
            roulet_wheel = self.gen_roulet_wheel(prop_pos)
            for i in range(self.Lambda % 2):
                pnts = self.choose_parents(roulet_wheel)
                if self.log:
                    print(f'Chose parents: \n{pnts}')
                chln = self.gen_children(P[pnts[0]], P[pnts[1]])
                chln = [self.mutate(chln[0]), self.mutate(chln[1])]
                if self.log:
                    print(f'Generated children: \n{chln}')
                P.extend(chln)
            P = self.select_new_pop(P)
            if self.log:
                print(f'Selected new population: \n{P}')
            if temp_best_score < best_score:
                if self.log:
                    print(f'Best score improved: \n{temp_best_score}\n')
                best_score, h_const_count = temp_best_score, 0
            else:
                if self.log:
                    print(f'Best score was not improved\n')
                h_const_count += 1
            h_count += 1
        if self.log:
            if h_const_count >= self.H_maxconst:
                print(
                    f'Exit: best score not improving for {self.H_maxconst} iterations: {best_score}')
            elif h_count >= self.H_max:
                print(
                    f'Exit: max iterations reached with best score: {best_score}')
        lang_genes = [i for i in range(len(best_pers)) if best_pers[i] == 1]
        return self.L[lang_genes[0]], self.L[lang_genes[1]], best_score

    def goal_func(self, chromo):
        T = self.T
        lang_genes = [i for i in range(len(chromo)) if chromo[i] == 1]
        A = lang_genes[0]
        B = lang_genes[1]
        n1, n2, n3, n4 = 0, 0, 0, 0
        for j in range(len(T)):
            n1_j = 1 if T[j][A] + T[j][B] == 2 else 0
            n2_j = 1 if T[j][A] - T[j][B] == 1 else 0
            n3_j = 1 if T[j][B] - T[j][A] == 1 else 0
            n4_j = 1 if T[j][A] + T[j][B] == 0 else 0
            n1, n2, n3, n4 = n1+n1_j, n2+n2_j, n3+n3_j, n4+n4_j
        n_max = max(n1, n2, n3, n4)
        n_min = min(n1, n2, n3, n4)
        return n_max - n_min

    def calc_ideal(self, chromo):
        chromoVal = self.goal_func(chromo)
        return [chromoVal, chromoVal == 0]

    def gen_pop_shot_gun(self):
        P = []
        for i in range(self.Mu):
            gen1 = random.randint(0, self.m-1)
            gen2 = gen1
            while gen1 == gen2:
                gen2 = random.randint(0, self.m-1)
            chromo = [0] * self.m
            chromo[gen1], chromo[gen2] = 1, 1
            P.append(chromo)
        P.sort(key=lambda e: self.goal_func(e))
        return P

    def calc_prop_pos(self, P):
        goal_vals = []
        sum_val = 0
        for chromo in P:
            val = self.goal_func(chromo)
            sum_val += val
            goal_vals.append(val)
        prop_pos = [[i, goal_vals[i]/sum_val] for i in range(len(goal_vals))]
        return prop_pos

    def gen_roulet_wheel(self, prop_pos):
        wheel = []
        for pp in prop_pos:
            wheel.extend([pp[0]] * int(round((round(pp[1], 3)*self.ws), 0)))
        return wheel

    def choose_parents(self, wheel):
        pnt1_i = random.randint(0, len(wheel)-1)
        pnt2_i = pnt1_i
        while wheel[pnt1_i] == wheel[pnt2_i]:
            pnt2_i = random.randint(0, len(wheel)-1)
        return [wheel[pnt1_i], wheel[pnt2_i]]

    def gen_children(self, pnt1, pnt2):
        pnt1_genes = [i for i in range(len(pnt1)) if pnt1[i] == 1]
        pnt2_genes = [i for i in range(len(pnt2)) if pnt2[i] == 1]
        cross = [max(pnt1_genes[0], pnt2_genes[0]),
                 min(pnt1_genes[1], pnt2_genes[1])]
        if pnt1_genes == cross or pnt1_genes[1] == pnt2_genes[1]:
            cross = [pnt2_genes[0], pnt1_genes[0]]
        elif pnt2_genes == cross or pnt1_genes[0] == pnt2_genes[0]:
            cross = [pnt2_genes[1], pnt1_genes[1]]
        cross.sort()
        child1, child2 = copy(pnt1), copy(pnt2)
        child1[cross[0]: cross[1]+1] = pnt2[cross[0]: cross[1]+1]
        child2[cross[0]: cross[1]+1] = pnt1[cross[0]: cross[1]+1]
        return [child1, child2]

    def mutate(self, chromo):
        chromo = copy(chromo)
        lang_genes = [i for i in range(len(chromo)) if chromo[i] == 1]
        mut_pt1 = lang_genes[random.randint(0, 1)]
        mut_pt2 = mut_pt1
        while chromo[mut_pt2] == 1:
            mut_pt2 = random.randint(0, len(chromo)-1)
        if random.uniform(0, 1) > 0.5:
            chromo[mut_pt1] = 0
            chromo[mut_pt2] = 1
        return chromo

    def select_new_pop(self, P):
        P.sort(key=lambda e: self.goal_func(e))
        return P[0: self.Mu]
