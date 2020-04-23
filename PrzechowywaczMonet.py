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