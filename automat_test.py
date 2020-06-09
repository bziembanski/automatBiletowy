import unittest
import automat


class AutomatTest(unittest.TestCase):
    def test_odliczona_kwota(self):
        a = automat.Automat(automat.LISTA_NOMINALOW)
        b = automat.Bilet(50, "ulgowy", 240)
        a.dodaj_bilet(b)
        a.wrzuc_monety(200)
        a.wrzuc_monety(20, 2)
        self.assertEqual(a.zaplac(), {})

    def test_udane_wydanie_reszty(self):
        a = automat.Automat(automat.LISTA_NOMINALOW)
        b = automat.Bilet(50, "ulgowy", 240)
        a.napelnij(2)
        a.dodaj_bilet(b)
        a.wrzuc_monety(500)
        reszta = a.zaplac()
        self.assertEqual(a.suma_monet(reszta), 260)

    def test_nieudane_wydanie_reszty(self):
        a = automat.Automat(automat.LISTA_NOMINALOW)
        b = automat.Bilet(60, "ulgowy", 240)
        a.dodaj_bilet(b)
        a.wrzuc_monety(500)
        wrzucone = a.wrzucone.copy()
        zwrocone = a.zaplac()
        self.assertEqual(zwrocone, wrzucone)

    def test_wrzucanie_po_1gr_1(self):
        a = automat.Automat(automat.LISTA_NOMINALOW)
        for _ in range(100):
            a.wrzuc_monety(1)
        self.assertEqual(a.suma_monet(), 100)

    def test_dwa_rozne_bilety(self):
        a = automat.Automat(automat.LISTA_NOMINALOW)
        a.dodaj_bilet(automat.Bilet(60, "ulgowy", 240))
        a.dodaj_bilet(automat.Bilet(60, "normalny", 480))
        self.assertEqual(a.do_zaplaty(), 240 + 480)

    def test_operacje_naprzemian(self):
        a = automat.Automat(automat.LISTA_NOMINALOW)
        a.dodaj_bilet(automat.Bilet(60, "ulgowy", 240))
        a.wrzuc_monety(500)
        a.wrzuc_monety(10)
        a.dodaj_bilet(automat.Bilet(40, "normalny", 380))
        a.wrzuc_monety(100)
        a.wrzuc_monety(10)
        zwrocone = a.zaplac()
        self.assertEqual(zwrocone, {})

    def test_ujemna_ilosc_monet(self):
        a = automat.Automat(automat.LISTA_NOMINALOW)
        check = a.wrzuc_monety(1, -2)
        self.assertEqual(check, False)

    def test_niecalkowita_ilosc_monet(self):
        a = automat.Automat(automat.LISTA_NOMINALOW)
        check = a.wrzuc_monety(1, 2.5)
        self.assertEqual(check, False)


if __name__ == '__main__':
    unittest.main()
