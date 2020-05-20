from math import floor

LISTA_NOMINALOW = [1, 2, 5, 10, 20, 50,
                   100, 200, 500, 1000, 2000, 5000]


class Bilet:
    def __init__(self, dlugosc, typ):
        self._dlugosc = dlugosc
        self._typ = typ

    def wyswietl_bilet(self):
        print(f"Bilet {self._typ} {self._dlugosc}-minutowy")

    def get_dlugosc(self):
        return self._dlugosc

    def get_typ(self):
        return self._typ


class Automat:
    def __init__(self, nominaly):
        self._zawartosc = {x: 0 for x in nominaly}

    def wrzuc_monety(self, moneta, ilosc):
        if moneta in self._zawartosc:
            self._zawartosc[moneta] += ilosc
        else:
            print(f'Automat nie obsługuje nominału {moneta}')

    def napelnij(self, ile=100):
        for i in self._zawartosc:
            self._zawartosc[i] = ile

    def pokaz_monety(self):
        for i, j in self._zawartosc.items():
            print(f'{i / 100}zł\t{j}')

    def laczna_kwota(self, dic=None):
        suma = 0
        if dic is None:
            dic = self._zawartosc
        for nominal, ilosc in dic.items():
            suma += nominal * ilosc
        return suma / 100

    def wydaj_reszte(self, kwota):
        do_wydania = int(kwota * 100)  # zamiana na grosze
        if self.laczna_kwota() < kwota:
            return {}

        nominaly = [*self._zawartosc]
        nominaly.reverse()
        # print(nominaly)
        reszta = {}
        i = 0
        while do_wydania > 0 and i < len(nominaly):
            if do_wydania >= nominaly[i]:
                ile = floor(do_wydania / nominaly[i])
                if ile > self._zawartosc[nominaly[i]]:
                    ile = self._zawartosc[nominaly[i]]
                do_wydania = round(100 * (do_wydania - (nominaly[i] * ile))) / 100
                reszta[nominaly[i]] = ile
                self._zawartosc[nominaly[i]] -= ile
            i += 1
        return reszta


def main():
    a = Automat(LISTA_NOMINALOW)
    a.napelnij(10)
    a.pokaz_monety()
    r = a.wydaj_reszte(6.99)
    print(a.laczna_kwota(r))
    a.pokaz_monety()


if __name__ == '__main__':
    main()
