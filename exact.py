class Exact:
    def __init__(self, L, T, log=False):
        self.L = L
        self.T = T
        self.m = len(L)
        self.log = log

    def apply(self):
        if(self.log):
            print('\n*** Exact Algorithm ***')
        LPairs = self.__find_all_pairs()
        bestSol = None
        goalVals = None
        for i in range(len(LPairs)):
            A, B = LPairs[i][0], LPairs[i][1]
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
            value = nMax - nMin
            if self.log:
                print(f'({self.L[A]},{self.L[B]}), F = {value}')
            if bestSol == None or value < bestSol:
                bestSol = value
                goalVals = [A, B]
        if self.log:
            print(
                f'\nResult: A,B=({self.L[goalVals[0]]},{self.L[goalVals[1]]}), F = {bestSol}')
        return self.L[goalVals[0]], self.L[goalVals[1]], bestSol

    def __find_all_pairs(self):
        pairs = []
        for i in range(self.m):
            for j in range(i+1, self.m):
                pairs.append([i, j])
        return pairs
