"""Ten moduł zawiera logikę pozwalającą na symulację pracy automatu biletowego.

Classes:
    Bilet
        Reprezentuje bilety kupowane w automacie.
    Automat
        Zawiera całą logikę odpowiedzialną za pracę automatu.
"""

LISTA_NOMINALOW = [1, 2, 5, 10, 20, 50,
                   100, 200, 500, 1000, 2000, 5000]
"""list: Lista zawierające domyślne nominały używane w automacie."""
DLUGOSC_BILETU_MINUTY = [20, 40, 60]
"""list: Lista zawierająca domyślne długości biletów"""
CENA_BILETU = [280, 380, 500]
"""list: Lista zawierająca domyślne ceny biletów"""
TYP_BILETU = ["normalny", "ulgowy"]
"""list: Lista zawierająca domyślne typy biletów"""


class Bilet:
    """
    Klasa przedstawiająca bilet komunikacji miejskiej.

    dlugosc : int
        Określa długość biletu w minutach. Możliwe opcje przechowywane w liście
        DLUGOSC_BILETU_MINUTY.
    typ : string
        Określa typ biletu. Możliwe opcje przechowywane w liście TYP_BILETU.
    cena:  int
        Określa cenę biletu. Możliwe opcje przechowywane w liście CENA_BILETU.
    """

    def __init__(self, dlugosc, typ, cena):
        self.dlugosc = dlugosc
        self.typ = typ
        self.cena = cena

    def __eq__(self, other):
        return self.dlugosc == other.dlugosc and self.typ == other.typ \
               and self.cena == other.cena

    def __str__(self):
        return f"Bilet {self.typ} {self.dlugosc}-minutowy"

    def __repr__(self):
        return f'Bilet({self.dlugosc}, "{self.typ}", {self.cena})'


class Automat:
    """
    Klasa symulująca pracę automatu biletowego komunikacji miejskiej.

    Attributes:

    _nominaly : list
        Lista zwierająca listę nominałów obsługiwanych przez automat.
    _bilety : list
        Lista zawierająca bilety, które kupujący zamierza nabyć.
    _zawartosc : dict
        Słownik określający liczbę monet danego nominału,
        które są dostępne w automacie.
    _wrzucone : dict
        Słownik określający liczbę monet danego nominału,
        które zostały wrzucone przez kupującego.

    Methods:

    wrzuc_monety(moneta, ilosc)
        Wrzuca określoną liczbę monet danego nominału
    napelnij(ile)
        Wrzuca ustaloną liczbę monet każdego typu do automatu.
    pokaz_monety(dic)
        Zwraca string przedstawiający monety wrzucone przez kupującego
        lub string przedstawiający monety w słowniku przekazanym do metody.
    suma_monet(dic)
        Zwraca sumę monet wrzuconych przez kupującego
        lub sumę monet w słowniku przekazanym do metody.
    suma zawartosci()
        Zwraca sumę monet w automacie.
    dodaj_bilet(bilet, ile)
        Dodaje podaną ilość danego biletu do automatu.
    usun_bilet(bilet)
        Usuwa podany bilet z automatu.
    usun_bilet_all()
        Usuwa wszystkie bilety z automatu.
    do_zaplaty()
        Zwraca sumaryczną kwotę za bilety.
    wydaj_reszte()
        Oblicza resztę oraz zwraca ilosc monet oraz słownik z wydaną resztą.
    zaplac()
        Konczy transakcję pobierając monety,
        zwracając resztę i usuwając bilety z automatu."""

    def __init__(self, nominaly):
        """
        Ustawia wartości początkowe dla parametrów automatu

        :param nominaly: Lista nominałów obsługiwana przez automat.
        """
        self.nominaly = nominaly
        self.zawartosc = {x: 0 for x in self.nominaly}
        self.bilety = []
        self.wrzucone = {x: 0 for x in self.nominaly}

    def wrzuc_monety(self, moneta, ilosc=1):
        """
        Wrzuca określoną liczbę podanych monet.

        :param moneta: Określa nominał wrzucanej monety.
        :param ilosc: Określa liczbę wrzucanych monet.
        :return:
            Zwraca True jeśli podana moneta jest obsługiwana przez automat
            lub Fałsz w przeciwnym wypadku."""
        if ilosc > 0 and ilosc == int(ilosc):
            if moneta in self.wrzucone:
                self.wrzucone[moneta] += ilosc
                return True
            print(f'Automat nie obsługuje nominału {moneta}!')
            return False
        print('Wprowadz ilosc jako dodatnią liczbę całkowitą!')
        return False

    def napelnij(self, ile=100):
        """
        Wrzuca ustaloną liczbę monet każdego typu do automatu.

        :param ile: Ile monet ma zostać wrzuconych.
        """
        for i in self.zawartosc:
            self.zawartosc[i] = ile

    def pokaz_monety(self, dic=None):
        """
        Zwraca string przedstawiający monety wrzucone przez kupującego
        lub string przedstawiający monety w słowniku przekazanym do metody.

        :param dic: Opcjonaly słownik który ma zostać przedstawiony w stringu
        :return: String z znakową reprezentacją monet.
        """
        pokaz_str = ''
        if dic is None:
            dic = self.wrzucone
        for i, j in dic.items():
            if j != 0:
                pokaz_str += '{:2.2f}zł: {}\t'.format(i / 100, j)
        return pokaz_str

    def suma_monet(self, dic=None):
        """
        Zwraca sumę monet wrzuconych przez kupującego
        lub sumę monet w słowniku przekazanym do metody.
        :param dic: Opcjonaly słownik z monetami, który ma być zsumowany.
        :return: Suma monet w groszach.
        """
        suma = 0
        if dic is None:
            dic = self.wrzucone
        for nominal, ilosc in dic.items():
            suma += nominal * ilosc
        return suma

    def suma_zawartosc(self):
        """
        Zwraca sumę monet w automacie.

        :return: Suma monet w automacie.
        """
        suma = 0
        for nominal, ilosc in self.zawartosc.items():
            suma += nominal * ilosc
        return suma

    def dodaj_bilet(self, bilet, ile=1):
        """
        Dodaje podaną ilość danego biletu do automatu.

        :param bilet: Bilet który ma zostać dodany.
        :param ile: Liczba ile biletów ma zostać dodanych.
        """
        for _ in range(ile):
            self.bilety.append(bilet)

    def usun_bilet(self, bilet):
        """
        Usuwa podany bilet z automatu.

        :param bilet: Bilet który ma zostać usunięty.
        """
        if bilet in self.bilety:
            self.bilety.remove(bilet)

    def usun_bilet_all(self):
        """
         Usuwa wszystkie bilety z automatu
        """
        self.bilety.clear()

    def do_zaplaty(self):
        """
         Zwraca sumaryczną kwotę za bilety.

        :return: Kwota do zapłaty groszach.
        """
        return sum(bilet.cena for bilet in self.bilety)

    def wydaj_reszte(self):
        """
        Oblicza resztę oraz zwraca ilosc monet oraz słownik z wydaną resztą.

        :return:
            Krotka z liczbą wydanych monet oraz słownikiem zawierającym resztę.
            """
        max_i = 999999999
        coins_used = []
        min_coins = []
        limit = list(self.zawartosc.values())
        coins = list(self.zawartosc.keys())
        reszta = self.suma_monet() - self.do_zaplaty()
        for i in range(reszta + 1):
            coins_used.append([])
            for j in range(len(self.zawartosc.items())):
                coins_used[i].append(0)
        min_coins.append(0)
        for i in range(reszta):
            min_coins.append(max_i)
        for i, coin in enumerate(coins):
            while limit[i] > 0:
                for j in reversed(range(reszta)):
                    curr_amount = j + coin
                    if curr_amount <= reszta:
                        if min_coins[curr_amount] > min_coins[j] + 1:
                            min_coins[curr_amount] = min_coins[j] + 1
                            coins_used[curr_amount] = coins_used[j].copy()
                            coins_used[curr_amount][i] += 1
                limit[i] -= 1
        if min_coins[reszta] == max_i:
            return 0, {x: 0 for x in self.nominaly}
        return min_coins[reszta], dict(zip(coins, coins_used[reszta]))

    def zaplac(self):
        """Konczy transakcję pobierając monety,
        zwracając resztę i usuwając bilety z automatu.

        :return:
            Słownik bez monet jeśli zapłacono i nie była potrzeba wydać
            reszty. Słownik z monetami wrzuconymi przez kupującego jeśli nie
            można było wydać reszty. Słownik z wydaną resztą jeśli można było
            wydać resztę. Pusty słownik jeśli wprowadzona kwota nie wystarczała
            na zakup wybranych biletów."""
        if self.suma_monet() < self.do_zaplaty():
            # print("Wprowadzono niepełną kwotę!")
            return {}
        reszta = self.suma_monet() - self.do_zaplaty()
        if reszta == 0:
            for nominal, ilosc in self.wrzucone.items():
                self.zawartosc[nominal] += ilosc
            self.wrzucone = {x: 0 for x in self.nominaly}
            self.bilety.clear()
            print(self.bilety)
            return self.wrzucone
        czy_moge, reszta_dict = self.wydaj_reszte()
        if czy_moge == 0:
            # print("Tylko odliczona kwota")
            wrzucone = self.wrzucone.copy()
            self.wrzucone = {x: 0 for x in self.nominaly}
            self.bilety.clear()
            return wrzucone
        for coin in self.nominaly:
            self.zawartosc[coin] += self.wrzucone[coin]
            self.zawartosc[coin] -= reszta_dict[coin]
        self.bilety = []
        self.wrzucone = {x: 0 for x in self.nominaly}
        return reszta_dict
