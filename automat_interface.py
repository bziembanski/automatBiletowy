"""Ten moduł zawiera interfejs automatu biletowego z modułu 'automat'

Classes:
    OknoMonety
        Ta klasa definiuje okno w którym kupujący wrzuca monety
    AutomatApplication
        Ta klasa definiuje cały interfejs służący do obsługi automatu.
"""
import tkinter as tk
import tkinter.font as tk_font
import tkinter.messagebox as tk_messagebox
import automat


def update_var(variable: tk.IntVar, string_variable: tk.StringVar):
    """
    Funkcja służąc do aktualizowania zmiennej w wrapperze modułu tkinter.

    :param variable: Zmienna przchowująca wartość liczbową.
    :param string_variable: Zmienna interpretująca podaną wartośc liczbową.
    """
    string_variable.set('{:.2f}zł'.format(variable.get() / 100))


class OknoMonety:
    """
    Ta klasa definiuje okno w którym kupujący wrzuca monety.

    Attributes:

    top : TopLevel
        Okno z wyborem monet.
    parent
        Rodzic okna, główne okno interfejsu.
    coin_label : list
        Lista zawierająca widgety Label
        dla każdego nominału obsługiwanego przez automat.
    coin_spinbox : list
         Lista zawierająca widgety Spinbox
         dla każdego nominału obsługiwanego przez automat.
    coin_count : dict
        Słownik zawierająca monety wrzucone przez użytkownika.
    ok_button : tk.Button
        Przycisk potwierdzający wrzucone monety.

    Methods:

    ok(x_button)
        Funkcja zamykjąca okno, oraz potwierdzająca wrzucane monety.
    create_and_configure_widgets()
        Metoda wykonywana podczas zamykania okna przyciskiem 'OK' lub 'X'.
    """

    def __init__(self, parent):
        """
        Inicjalizuje okno oraz widgety, które się na nim znajdują.

        :param parent: Rodzic tworzonego okna.
        """
        self.top = tk.Toplevel(parent)
        self.top.grid_columnconfigure(0, minsize=50)
        self.top.grid_columnconfigure(2, minsize=50)
        self.top.grid_columnconfigure(3, minsize=100)
        self.top.resizable(False, False)
        self.top.protocol('WM_DELETE_WINDOW', lambda: self.ok_action(True))
        self.top.title("Wrzuć monety")
        self.parent = parent
        self.coin_label = []
        self.coin_spinbox = []
        self.coin_count = {}
        self.ok_button = tk.Button(self.top, text="Ok",
                                   command=lambda: self.ok_action(False))
        self.create_and_configure_widgets()

    def create_and_configure_widgets(self):
        """Tworzy oraz konfiguruje widgety używane w oknie."""
        for coin in automat.LISTA_NOMINALOW:
            self.coin_count[coin] = tk.IntVar(
                value=self.parent.automat.wrzucone[coin])
            self.coin_label.append(
                tk.Label(self.top, text=f'{coin / 100:.2f}zl'))
            self.coin_spinbox.append(
                tk.Spinbox(self.top, width=5, from_=0, to=100,
                           textvariable=self.coin_count[coin], state="readonly",
                           bg='white',
                           fg='black'))
        for i, coin in enumerate(zip(self.coin_spinbox, self.coin_label)):
            coin[1].grid(column=1, row=i, sticky=tk.N + tk.S + tk.E + tk.W)
            coin[0].grid(column=3, row=i, sticky=tk.N + tk.S + tk.E + tk.W)
        self.ok_button.grid(row=len(self.coin_spinbox) + 1, column=3,
                            sticky=tk.N + tk.S + tk.E + tk.W)
        self.top.update_idletasks()
        window_width = self.top.winfo_width()
        window_height = self.top.winfo_height()
        x_pos = (self.top.winfo_screenwidth() // 2) - (window_width // 2)
        y_pos = (self.top.winfo_screenheight() // 2) - (window_height // 2)
        self.top.geometry(
            '{}x{}+{}+{}'.format(window_width, window_height, x_pos, y_pos))

    def ok_action(self, x_button: bool):
        """Metoda wykonywana podczas zamykania okna przyciskiem 'OK' lub 'X'.

        :param x_button:
            Bool informujący czy użytkownik potwierdził monety przyciskiem 'OK',
            czy zamknął okno przyciskiem 'X'.
        """
        if not x_button:
            for coin in automat.LISTA_NOMINALOW:
                self.parent.automat.wrzucone[coin] = self.coin_count[coin].get()
        self.parent.wrzucanie_monet = False
        self.top.destroy()


class AutomatApplication(tk.Frame):
    """
    Klasa definiująca cały interfejs służący do obsługi automatu.

    Attributes:

    wrzucanie_monet : bool
        Określa czy otwarte jest obecnie okno wrzucania monet.
    automat : Automat
        Instancja automatu.
    do_zaplaty tk.IntVar
        Obecna kwota do zapłaty.
    wplacone tk.IntVar
        Obecna kwota wpłacona przez kupującego.
    do_zaplaty_string : tk.StringVar
        Kwota interpretująca do_zaplaty jako string do wyświetlenia.
    wplacone_string : tk.StringVar
        Kwota interpretująca wplacone jako string do wyświetlenia.
    do_zaplaty_desc_label : tk.Label
        Label z opisujący 'do_zaplaty_label'.
    wplacone_desc_label : tk.Label
        Label z opisujący 'wplacone_label'.
    do_zaplaty_label : tk.Label
        Label zawierający wartość z 'do_zaplaty_string'.
    wplacone_label.
        Label zawierający wartość z 'wplacone_string'.
    bilety_label : list
        Lista zawierająca tk.Label dla każdego typu biletu.
    bilety_spinbox : list
        Lista zawierająca tk.Spinbox dla każdego typu biletu.
    bilety_count : dict
        Słownik przechowujący tk.IntVar dla każdego typu biletu.
    wrzuc_monety_button : tk.Button
        Przycisk odpowiedzialny za otwieranie okna OknoCoin.
    zaplac_button : tk.Button
        Przyscik odpowiedzialny za zakończenie transakcji.
    zakoncz_button : tk.Button
        Przycisk zamykający głowne okno.

    Methods:

    wrzuc_monety_action()
        Metoda wywoływana przez przycisk 'wrzuc_monety_button'.
        Otwiera okno klasy 'OknoMonety', oraz wplaca potwierdzone monety.
    create_widgets()
        Metoda tworząca oraz konfigurująca widgety używane na oknie.
    odswiez_bilet()
        Metoda aktualizująca ilość biletów wybranych przez użytkownika
        oraz łączną kwotę do zapłaty za nie.
    zeruj_zakupy()
        Metoda resetująca liczbę biletów, wybrane monety,
        łączną cenę oraz wpłaconą kwotę.
    zaplac()
        Metoda wykonująca metodę 'zaplac' obiektu automat.
    """

    def __init__(self, master=None, napelnij=0):
        """
        Inicjalizuje okno aplikacji oraz widgety zawierające się w nim.

        :param master: Rodzic okna
        :param napelnij: Liczba początkowa monet w automacie.
        """
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.wrzucanie_monet = False
        self.automat = automat.Automat(automat.LISTA_NOMINALOW)
        self.automat.napelnij(napelnij)
        self.do_zaplaty = tk.IntVar(value=self.automat.do_zaplaty())
        self.wplacone = tk.IntVar(value=self.automat.suma_monet())
        self.do_zaplaty_string = tk.StringVar(
            value='{:.2f}zł'.format(self.do_zaplaty.get() / 100))
        self.wplacone_string = tk.StringVar(
            value='{:.2f}zł'.format(self.wplacone.get() / 100))
        self.do_zaplaty_desc_label = tk.Label(self, text="Kwota do zapłaty:",
                                              font=tk_font.Font(size=11),
                                              anchor='w')
        self.wplacone_desc_label = tk.Label(self, text="Kwota wpłacona:",
                                            font=tk_font.Font(size=11),
                                            anchor='w')
        self.do_zaplaty_label = tk.Label(self,
                                         textvariable=self.do_zaplaty_string)
        self.wplacone_label = tk.Label(self, textvariable=self.wplacone_string)
        self.bilety_label = []
        self.bilety_spinbox = []
        self.bilety_count = {
            typ: {f'{bilet[0]},{int(bilet[1] / (i + 1))}': tk.IntVar(value=0)
                  for bilet in
                  zip(automat.DLUGOSC_BILETU_MINUTY, automat.CENA_BILETU)} for
            i, typ in enumerate(automat.TYP_BILETU)}
        self.wrzuc_monety_button = tk.Button(self, text="Wrzuć monety",
                                             command=self.wrzuc_monety_action)
        self.zaplac_button = tk.Button(self, text="Zapłać", command=self.zaplac)
        self.zakoncz_button = tk.Button(self, text="Zakończ", command=self.quit)
        self.create_widgets()

    def wrzuc_monety_action(self):
        """
        Metoda wywoływana przez przycisk 'wrzuc_monety_button'.
        Otwiera okno klasy 'OknoMonety', oraz wplaca potwierdzone monety.
        """
        if not self.wrzucanie_monet:
            self.wrzucanie_monet = True
            wrzuc_monety_window = OknoMonety(self)
            self.wait_window(wrzuc_monety_window.top)
            self.wplacone.set(self.automat.suma_monet())
            update_var(self.wplacone, self.wplacone_string)

    def create_widgets(self):
        """
        Metoda tworząca oraz konfigurująca widgety używane na oknie.
        """
        self.do_zaplaty_desc_label.grid(column=0, row=0,
                                        sticky=tk.N + tk.S + tk.E + tk.W)
        self.wplacone_desc_label.grid(column=0, row=1,
                                      sticky=tk.N + tk.S + tk.E + tk.W)
        self.do_zaplaty_label.grid(column=1, row=0,
                                   sticky=tk.N + tk.S + tk.E + tk.W)
        self.wplacone_label.grid(column=1, row=1,
                                 sticky=tk.N + tk.S + tk.E + tk.W)
        for i, typ in enumerate(automat.TYP_BILETU):
            self.bilety_label.append(
                [tk.Label(self, text=f'{bilet[0]}-minutowy {typ}\n'
                                     f'{bilet[1] / 100 / (i + 1):.2f}zł')
                 for j, bilet
                 in enumerate(zip(automat.DLUGOSC_BILETU_MINUTY,
                                  automat.CENA_BILETU))])
            self.bilety_spinbox.append(
                [tk.Spinbox(self, from_=0, to=100,
                            textvariable=self.bilety_count[typ][
                                f'{bilet[0]},{int(bilet[1] / (i + 1))}'],
                            state="readonly",
                            bg='white', fg='black', command=self.odswiez_bilet)
                 for j, bilet
                 in enumerate(zip(automat.DLUGOSC_BILETU_MINUTY,
                                  automat.CENA_BILETU))])

        for i, typ in enumerate(zip(self.bilety_label, self.bilety_spinbox)):
            for j, bilet in enumerate(zip(typ[0], typ[1])):
                bilet[1].grid(row=(5 + 2 * i), column=j,
                              sticky=tk.N + tk.S + tk.E + tk.W)
                bilet[0].grid(row=(4 + 2 * i), column=j,
                              sticky=tk.N + tk.S + tk.E + tk.W)

        tk.Label(self, text="Dostępne bilety:",
                 font=tk_font.Font(size=13)).grid(row=3, column=0, columnspan=3)

        self.wrzuc_monety_button.grid(row=0, column=2,
                                      sticky=tk.N + tk.S + tk.E + tk.W)

        self.zaplac_button.grid(row=8, column=0,
                                sticky=tk.N + tk.S + tk.E + tk.W)

        self.zakoncz_button.grid(row=8, column=2,
                                 sticky=tk.N + tk.S + tk.E + tk.W)

    def odswiez_bilet(self):
        """
        Metoda aktualizująca ilość biletów wybranych przez użytkownika
        oraz łączną kwotę do zapłaty za nie.
        """
        self.automat.usun_bilet_all()
        for typ, bilet in self.bilety_count.items():
            for dlugosc_cena, ile in bilet.items():
                dlugosc, cena = dlugosc_cena.split(',')
                self.automat.dodaj_bilet(automat.Bilet(dlugosc, typ, int(cena)),
                                         ile.get())
        self.do_zaplaty.set(self.automat.do_zaplaty())
        update_var(self.do_zaplaty, self.do_zaplaty_string)

    def zeruj_zakupy(self):
        """
        Metoda resetująca liczbę biletów, wybrane monety,
        łączną cenę oraz wpłaconą kwotę.
        """
        for _, bilet in self.bilety_count.items():
            for _, ile in bilet.items():
                ile.set(0)
        self.wplacone.set(self.automat.suma_monet())
        self.do_zaplaty.set(self.automat.do_zaplaty())
        update_var(self.wplacone, self.wplacone_string)
        update_var(self.do_zaplaty, self.do_zaplaty_string)

    def zaplac(self):
        """
        Metoda wykonująca metodę 'zaplac' obiektu automat.
        """
        if self.do_zaplaty.get() > 0:
            wrzucone = self.automat.wrzucone.copy()
            bilety = self.automat.bilety.copy()
            zaplacone = self.automat.zaplac()

            if zaplacone == {}:
                tk_messagebox.showerror("Za mało gotówki!",
                                        "Wprowadzono niepełną kwotę!")
            else:
                if zaplacone == wrzucone:
                    tk_messagebox.showerror("Tylko odliczona kwota!",
                                            f'Tylko odliczona '
                                            f'kwota!\nWrzucona gotówka:\n'
                                            f'{self.automat.pokaz_monety(wrzucone)}\n')
                    self.zeruj_zakupy()

                elif zaplacone == {n: 0 for n in automat.LISTA_NOMINALOW}:
                    zakupione = ''
                    for bilet in bilety:
                        zakupione += f'\n{bilet}'
                    tk_messagebox.showinfo("Zakupy pomyślne",
                                           f"Zakupione bilety:{zakupione}\n"
                                           f"Łączna kwota: {self.do_zaplaty_string.get()}")
                    self.zeruj_zakupy()

                else:
                    zakupione = ''
                    for bilet in bilety:
                        zakupione += f'\n{bilet}'
                    tk_messagebox.showinfo("Zakupy pomyślne",
                                           f"Zakupione bilety:{zakupione}\n"
                                           f"Łączna kwota: {self.do_zaplaty_string.get()}\n"
                                           f"Reszta:{self.automat.suma_monet(zaplacone) / 100:.2f}zł")
                    self.zeruj_zakupy()
        else:
            tk_messagebox.showwarning("Wybierz bilety!",
                                      "Proszę wybrać bilety do zakupu!")


t = tk.Tk()
t.title('Automat biletowy')
a = AutomatApplication(t, 2)
t.resizable(False, False)
t.update_idletasks()
width = t.winfo_width()
height = t.winfo_height()
x = (t.winfo_screenwidth() // 2) - (width // 2)
y = (t.winfo_screenheight() // 2) - (height // 2)
t.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# a.master.title('Automat biletowy')
a.mainloop()
