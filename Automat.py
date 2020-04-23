from PrzechowywaczMonet import PrzechowywaczMonet
from Bilet import Bilet
class Automat(PrzechowywaczMonet):
    def __init__(self):
        super().__init__()
        pM = PrzechowywaczMonet()
        pM.wrzućMonety('1zł',3)
        pM.pokażMonety()