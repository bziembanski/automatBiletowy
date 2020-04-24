class Bilet():
    def __init__(self, długość, typ):
        self.długość = długość
        self.typ=typ
    def wyświetlBilet(self):
        print(f"Bilet {self.typ} {self.długość}-minutowy")


class PrzechowywaczMonet:
    def __init__(self):
        self._nominały = {'1gr': 0, '2gr': 0, '5gr': 0, '10gr': 0, '20gr': 0, '50gr': 0,
                    '1zł': 0, '2zł': 0, '5zł': 0, '10zł': 0, '20zł': 0, '50zł': 0}
    
    def wrzućMonety(self, moneta, ilosc):
        if moneta in self._nominały:
            self._nominały[moneta] += ilosc
        else:
            print(f'Automat nie obsługuje nominału {moneta}')

    def pokażMonety(self):
        for i, j in self._nominały.items():
            print(f'{i}\t{j}')

class Automat(PrzechowywaczMonet):
    def __init__(self):
        super().__init__()
        pM = PrzechowywaczMonet()
        pM.wrzućMonety('1zł',3)
        pM.pokażMonety()