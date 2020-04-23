class Bilet():
    def __init__(self, długość, typ):
        self.długość = długość
        self.typ=typ
    def wyświetlBilet(self):
        print(f"Bilet {self.typ} {self.długość}-minutowy")
    