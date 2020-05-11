from math import floor


class Bilet:
    def __init__(self, dlugosc, typ):
        self.dlugosc = dlugosc
        self.typ = typ

    def wyswietlBilet(self):
        print(f"Bilet {self.typ} {self.dlugosc}-minutowy")


class PrzechowywaczMonet:
    def __init__(self):
        self._nominaly = {1: 0, 2: 0, 5: 0, 10: 0, 20: 0, 50: 0,
                          100: 0, 200: 0, 500: 0, 1000: 0, 2000: 0, 5000: 0}

    def wrzucMonety(self, moneta, ilosc):
        if moneta in self._nominaly:
            self._nominaly[moneta] += ilosc
        else:
            print(f'Automat nie obsługuje nominału {moneta}')

    def napelnij(self):
        for i in self._nominaly:
            self._nominaly[i] = 100

    def pokazMonety(self):
        for i, j in self._nominaly.items():
            print(f'{i / 100}zł\t{j}')

    def lacznaKwota(self, dic=None):
        suma = 0
        if dic is None:
            dic = self._nominaly
        for nominal, ilosc in dic.items():
            suma += nominal * ilosc
        return suma / 100


class Automat(PrzechowywaczMonet):
    def __init__(self):
        super().__init__()

    def wydajReszte(self, kwota):
        doWydania = int(kwota * 100)  # zamiana na grosze
        if self.lacznaKwota() < kwota:
            return False
        else:
            nominaly = [*self._nominaly]
            nominaly.reverse()
            # print(nominaly)
            reszta = dict()
            i = 0
            while doWydania > 0 and i < len(nominaly):
                if doWydania >= nominaly[i]:
                    ile = floor(doWydania / nominaly[i])
                    if ile > self._nominaly[nominaly[i]]:
                        ile = self._nominaly[nominaly[i]]
                    doWydania = round(100 * (doWydania - (nominaly[i] * ile))) / 100
                    reszta[nominaly[i]] = ile
                    self._nominaly[nominaly[i]] -= ile
                i += 1
            return reszta


a = Automat()
a.napelnij()
a.pokazMonety()
reszta = a.wydajReszte(4.23)
print(a.lacznaKwota(reszta))
a.pokazMonety()
