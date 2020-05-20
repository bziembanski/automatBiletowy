from math import floor

LISTA_NOMINALOW = [1, 2, 5, 10, 20, 50,
                   100, 200, 500, 1000, 2000, 5000]


class Bilet:
    def __init__(self, dlugosc, typ, cena):
        self._dlugosc = dlugosc
        self._typ = typ
        self._cena = cena

    def wyswietl_bilet(self):
        print(f"Bilet {self._typ} {self._dlugosc}-minutowy - {self._cena / 100}")

    def get_dlugosc(self):
        return self._dlugosc

    def get_typ(self):
        return self._typ

    def get_cena(self):
        return self._cena

    def __eq__(self, other):
        return self._dlugosc == other._dlugosc and self._typ == other._typ and self._cena == other._cena

    def __repr__(self):
        return f'Bilet({self._dlugosc}, "{self._typ}", {self._cena})'


class Automat:
    def __init__(self, nominaly):
        self._zawartosc = {x: 0 for x in nominaly}
        self._bilety = []
        self._wrzucone = {x: 0 for x in nominaly}

    def wrzuc_monety(self, moneta, ilosc):
        if moneta in self._wrzucone:
            self._wrzucone[moneta] += ilosc
        else:
            print(f'Automat nie obsługuje nominału {moneta}')

    def napelnij(self, ile=100):
        for i in self._zawartosc:
            self._zawartosc[i] = ile

    def pokaz_monety(self, wrzucone=False):
        dic = self._zawartosc
        if wrzucone:
            dic = self._wrzucone
        for i, j in dic.items():
            print(f'{i / 100}zł\t{j}')

    def suma_monet(self, dic=None):
        suma = 0
        if dic is None:
            dic = self._wrzucone
        for nominal, ilosc in dic.items():
            suma += nominal * ilosc
        return suma

    def suma_zawartosc(self):
        suma = 0
        for nominal, ilosc in self._zawartosc.items():
            suma += nominal * ilosc
        return suma

    def wydaj_reszte(self, kwota):
        do_wydania = int(kwota * 100)  # zamiana na grosze
        if self.suma_zawartosc() < kwota:
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

    def dodaj_bilet(self, bilet):
        self._bilety.append(bilet)

    def usun_bilet(self, bilet):
        if bilet in self._bilety:
            self._bilety.remove(bilet)

    def do_zaplaty(self):
        return sum(bilet.get_cena() for bilet in self._bilety)


def main():
    a = Automat(LISTA_NOMINALOW)
    a.napelnij(10)
    a.pokaz_monety()
    r = a.wydaj_reszte(6.99)
    print(a.suma_monet(r))
    a.pokaz_monety()

    a.dodaj_bilet(Bilet(50, 'normalny', 400))
    a.dodaj_bilet(Bilet(30, 'normalny', 300))
    a.wrzuc_monety(500, 2)


if __name__ == '__main__':
    main()
