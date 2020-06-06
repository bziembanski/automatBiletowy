LISTA_NOMINALOW = [1, 2, 5, 10, 20, 50,
                   100, 200, 500, 1000, 2000, 5000]
DLUGOSC_BILETU_MINUTY = [20, 40, 60]
CENA_BILETU = [280, 380, 500]
TYP_BILETU = ["normalny", "ulgowy"]


class Bilet:
    def __init__(self, dlugosc, typ, cena):
        self.dlugosc = dlugosc
        self.typ = typ
        self.cena = cena

    def wyswietl_bilet(self):
        print(f"Bilet {self.typ} {self.dlugosc}-minutowy - {self.cena / 100}")

    def __eq__(self, other):
        return self.dlugosc == other.dlugosc and self.typ == other.typ and self.cena == other.cena

    def __repr__(self):
        return f'Bilet({self.dlugosc}, "{self.typ}", {self.cena})'


class Automat:
    def __init__(self, nominaly):
        self._nominaly = nominaly
        self._zawartosc = {x: 0 for x in self._nominaly}
        self._bilety = []
        self._wrzucone = {x: 0 for x in self._nominaly}

    def wrzuc_monety(self, moneta, ilosc=1):
        if ilosc > 0 and ilosc == int(ilosc):
            if moneta in self._wrzucone:
                self._wrzucone[moneta] += ilosc
                return True
            else:
                print(f'Automat nie obsługuje nominału {moneta}!')
                return False
        else:
            print('Wprowadz ilosc jako dodatnią liczbę całkowitą!')
            return False

    def napelnij(self, ile=100):
        for i in self._zawartosc:
            self._zawartosc[i] = ile

    def pokaz_monety(self, wrzucone=False):
        dic = self._wrzucone if wrzucone else self._zawartosc
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

    def dodaj_bilet(self, bilet, ile=1):
        for _ in range(ile):
            self._bilety.append(bilet)

    def usun_bilet(self, bilet):
        if bilet in self._bilety:
            self._bilety.remove(bilet)

    def do_zaplaty(self):
        return sum(bilet.cena for bilet in self._bilety)

    def wydaj_reszte(self):
        max_i = 999999999
        coins_used = []
        min_coins = []
        limit = list(self._zawartosc.values())
        coins = list(self._zawartosc.keys())
        reszta = self.suma_monet() - self.do_zaplaty()
        for i in range(reszta + 1):
            coins_used.append([])
            for j in range(len(self._zawartosc.items())):
                coins_used[i].append(0)
        min_coins.append(0)
        for i in range(reszta):
            min_coins.append(max_i)
        for i in range(len(coins)):
            while limit[i] > 0:
                for j in reversed(range(reszta)):
                    curr_amount = j + coins[i]
                    if curr_amount <= reszta:
                        if min_coins[curr_amount] > min_coins[j] + 1:
                            min_coins[curr_amount] = min_coins[j] + 1
                            coins_used[curr_amount] = coins_used[j].copy()
                            coins_used[curr_amount][i] += 1
                limit[i] -= 1
        if min_coins[reszta] == max_i:
            return 0, {x: 0 for x in self._nominaly}
        return min_coins[reszta], dict(zip(coins, coins_used[reszta]))

    def zaplac(self):
        if self.suma_monet() < self.do_zaplaty():
            print("Wprowadzono niepełną kwotę!")
            return {}
        reszta = self.suma_monet() - self.do_zaplaty()
        if reszta == 0:
            for nominal, ilosc in self._wrzucone.items():
                self._zawartosc[nominal] += ilosc
            self._bilety = []
            return {}
        else:
            czy_moge, reszta_dict = self.wydaj_reszte()
            if czy_moge == 0:
                print("Tylko odliczona kwota")
                wrzucone = self._wrzucone.copy()
                self._wrzucone = {x: 0 for x in self._nominaly}
                return wrzucone
            else:
                for n in self._nominaly:
                    self._zawartosc[n] += self._wrzucone[n]
                    self._zawartosc[n] -= reszta_dict[n]
                self._bilety = []
                self._wrzucone = {x: 0 for x in self._nominaly}
                return reszta_dict


def main():
    a = Automat(LISTA_NOMINALOW)
    a.napelnij(1)
    a.dodaj_bilet(Bilet(50, 'normalny', 400))
    a.dodaj_bilet(Bilet(30, 'normalny', 159))
    a.wrzuc_monety(500, 1)
    a.wrzuc_monety(50, 1)
    a.wrzuc_monety(5, 2)
    print(a.zaplac())


if __name__ == '__main__':
    main()
