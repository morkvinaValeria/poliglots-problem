import random


class LocalSearch:
    def __init__(self, L, T, log=False):
        self.L = L
        self.T = T
        self.m = len(L)
        self.Hmax = 0.45*self.m
        self.log = log

    def apply(self):
        if(self.log):
            print('\n\n*** Local Search ***\n')
        Ah, Bh = self.__generate_initial_languages()
        CritVal = self.__calculate_crit_val(Ah, Bh)
        if self.log:
            print(f'A0,B0=({ self.L[Ah]}, { self.L[Bh]}); F = {CritVal}')
        if(CritVal == 0):
            if self.log:
                print('Perfect case found, F = 0')
            return self.L[Ah], self.L[Bh], CritVal
        r = int(round(0.1*self.m + 1, 1))
        Delta = -1
        h = 0
        ExploredPairs = [[Ah, Bh]]
        while True:
            Oab = self.__generateO(Ah, Bh, r)
            if self.log:
                print(f'\nOab for ({ self.L[Ah]}, { self.L[Bh]}): {Oab}')
            i = h = 0
            Ay = By = Val = Delta = -1
            while Delta <= 0 and i < len(Oab) and h < self.Hmax and CritVal != 0:
                Ay, By = Oab[i][0], Oab[i][1]
                if([Ay, By] not in ExploredPairs):
                    Val = self.__calculate_crit_val(Ay, By)
                    Delta = CritVal - Val
                    if self.log:
                        print(
                            f'i = {h}   ({self.L[Ay]},{self.L[By]}), F = {Val};   ▲ = {Delta}')
                    h = h + 1
                    ExploredPairs.append([Ay, By])
                else:
                    if self.log:
                        print(
                            f'         ({self.L[Ay]},{self.L[By]}) was already explored')
                i = i + 1
            if (Delta > 0):
                if self.log:
                    print(f'Changing pair languages')
                CritVal = Val
                Ah, Bh = Ay, By
            if r < 0.25 * self.m+1:
                r = r+int(round(0.18*self.m, 0))
            if CritVal == 0 or Delta <= 0 or h >= self.Hmax:
                if self.log:
                    if(CritVal == 0):
                        print('Perfect case found, F = 0')
                    elif h >= self.Hmax:
                        print(f'Best score not improving for {h} iterations')
                    else:
                        print(f'\n Best score was not improved')
                    print(
                        f'\n\nResult: A,B=({self.L[Ah]},{self.L[Bh]}), F = {CritVal}')
                return self.L[Ah], self.L[Bh], CritVal

    def __generate_initial_languages(self):
        Ah = self.__choose_random_element(self.m)
        theSame = True
        Bh = None
        while(theSame):
            Bh = self.__choose_random_element(self.m)
            if (Ah != Bh):
                theSame = False
        return Ah, Bh

    def __choose_random_element(self, m):
        return random.randint(0, m - 1)

    def __calculate_crit_val(self, A, B):
        n1 = n2 = n3 = n4 = 0
        for j in range(len(self.T)):
            n1j = 1 if self.T[j][A] + self.T[j][B] == 2 else 0
            n2j = 1 if self.T[j][A] - self.T[j][B] == 1 else 0
            n3j = 1 if self.T[j][B] - self.T[j][A] == 1 else 0
            n4j = 1 if self.T[j][A] + self.T[j][B] == 0 else 0
            n1 = n1 + n1j
            n2 = n2 + n2j
            n3 = n3 + n3j
            n4 = n4 + n4j
        nMax = max(n1, n2, n3, n4)
        nMin = min(n1, n2, n3, n4)
        CritVal = nMax - nMin
        return CritVal

    def __generateO(self, A, B, r):
        Oab = []
        for i in range(1, r + 1):
            if abs(A - i) < self.m and abs(B - i) < self.m:
                Oab.append([A - i, B - i])
            if abs(A + i) < self.m and abs(B + i) < self.m:
                Oab.append([A + i, B + i])
        return Oab
