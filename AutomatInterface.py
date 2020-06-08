import tkinter as tk
import tkinter.font as tk_font
import tkinter.messagebox as tk_messagebox
import Automat as A


def updateVar(variable: tk.IntVar, string_variable: tk.StringVar):
    string_variable.set('{:.2f}zł'.format(variable.get() / 100))


class MyDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.grid_columnconfigure(0, minsize=50)
        top.grid_columnconfigure(2, minsize=50)
        top.grid_columnconfigure(3, minsize=100)
        top.resizable(False, False)
        self.top.protocol('WM_DELETE_WINDOW', lambda: self.ok(True))
        self.top.title("Wrzuć monety")
        self.parent = parent
        self.coin_label = []
        self.coin_spinbox = []
        self.coin_count = {}
        for c in A.LISTA_NOMINALOW:
            self.coin_count[c] = tk.IntVar(value=self.parent.automat._wrzucone[c])
            self.coin_label.append(tk.Label(top, text=f'{c / 100:.2f}zl'))
            self.coin_spinbox.append(
                tk.Spinbox(top, width=5, from_=0, to=100, textvariable=self.coin_count[c], state="readonly", bg='white',
                           fg='black'))
        for i, coin in enumerate(zip(self.coin_spinbox, self.coin_label)):
            coin[1].grid(column=1, row=i, sticky=tk.N + tk.S + tk.E + tk.W)
            coin[0].grid(column=3, row=i, sticky=tk.N + tk.S + tk.E + tk.W)

        self.ok_button = tk.Button(top, text="Ok", command=lambda: self.ok(False))
        self.ok_button.grid(row=len(self.coin_spinbox) + 1, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def ok(self, x_button):
        if not x_button:
            for c in A.LISTA_NOMINALOW:
                self.parent.automat._wrzucone[c] = self.coin_count[c].get()
        self.parent.wrzucanie_monet = False
        self.top.destroy()


class AutomatApplication(tk.Frame):
    def __init__(self, master=None, napelnij=0):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.wrzucanie_monet = False
        self.automat = A.Automat(A.LISTA_NOMINALOW)
        self.automat.napelnij(napelnij)
        self.do_zaplaty = tk.IntVar(value=self.automat.do_zaplaty())
        self.wplacone = tk.IntVar(value=self.automat.suma_monet())
        self.do_zaplaty_string = tk.StringVar(value='{:.2f}zł'.format(self.do_zaplaty.get() / 100))
        self.wplacone_string = tk.StringVar(value='{:.2f}zł'.format(self.wplacone.get() / 100))
        self.createWidgets()

    def wrzuc_monety(self):
        if not self.wrzucanie_monet:
            self.wrzucanie_monet = True
            d = MyDialog(self)
            self.wait_window(d.top)
            self.wplacone.set(self.automat.suma_monet())
            updateVar(self.wplacone, self.wplacone_string)

    def createWidgets(self):
        top = self.winfo_toplevel()

        self.do_zaplaty_desc_label = tk.Label(self, text="Kwota do zapłaty:", font=tk_font.Font(size=11), anchor='w')
        self.do_zaplaty_desc_label.grid(column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.wplacone_desc_label = tk.Label(self, text="Kwota wpłacona:", font=tk_font.Font(size=11), anchor='w')
        self.wplacone_desc_label.grid(column=0, row=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.do_zaplaty_label = tk.Label(self, textvariable=self.do_zaplaty_string)
        self.do_zaplaty_label.grid(column=1, row=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.wplacone_label = tk.Label(self, textvariable=self.wplacone_string)
        self.wplacone_label.grid(column=1, row=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.bilety_label = []
        self.bilety_spinbox = []
        self.bilety_count = {
            typ: {f'{bilet[0]},{int(bilet[1] / (i + 1))}': tk.IntVar(value=0) for bilet in
                  zip(A.DLUGOSC_BILETU_MINUTY, A.CENA_BILETU)} for
            i, typ in enumerate(A.TYP_BILETU)}
        for i, typ in enumerate(A.TYP_BILETU):
            self.bilety_label.append(
                [tk.Label(self, text=f'{bilet[0]}-minutowy {typ}\n{bilet[1] / 100 / (i + 1):.2f}zł') for j, bilet
                 in enumerate(zip(A.DLUGOSC_BILETU_MINUTY, A.CENA_BILETU))])
            self.bilety_spinbox.append(
                [tk.Spinbox(self, from_=0, to=100,
                            textvariable=self.bilety_count[typ][f'{bilet[0]},{int(bilet[1] / (i + 1))}'],
                            state="readonly",
                            bg='white', fg='black', command=self.odswiez_bilet) for j, bilet
                 in enumerate(zip(A.DLUGOSC_BILETU_MINUTY, A.CENA_BILETU))])

        for i, typ in enumerate(zip(self.bilety_label, self.bilety_spinbox)):
            for j, bilet in enumerate(zip(typ[0], typ[1])):
                bilet[1].grid(row=(5 + 2 * i), column=j, sticky=tk.N + tk.S + tk.E + tk.W)
                bilet[0].grid(row=(4 + 2 * i), column=j, sticky=tk.N + tk.S + tk.E + tk.W)

        tk.Label(self, text="Dostępne bilety:", font=tk_font.Font(size=13)).grid(row=3, column=0, columnspan=3)
        self.wrzuc_monety_button = tk.Button(self, text="Wrzuć monety", command=self.wrzuc_monety)
        self.wrzuc_monety_button.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.zaplac_button = tk.Button(self, text="Zapłać", command=self.zaplac)
        self.zaplac_button.grid(row=8, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.zakoncz_button = tk.Button(self, text="Zakończ", command=lambda: self.quit())
        self.zakoncz_button.grid(row=8, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

    def odswiez_bilet(self, zeruj=False):
        self.automat.usun_bilet_all()
        for typ, bilet in self.bilety_count.items():
            for dlugosc_cena, ile in bilet.items():
                dlugosc, cena = dlugosc_cena.split(',')
                self.automat.dodaj_bilet(A.Bilet(dlugosc, typ, int(cena)), ile.get())
        self.do_zaplaty.set(self.automat.do_zaplaty())
        updateVar(self.do_zaplaty, self.do_zaplaty_string)
        # self.do_zaplaty_string.set('{:.2f}zł'.format(self.do_zaplaty.get() / 100))

    def zeruj_zakupy(self):
        for typ, bilet in self.bilety_count.items():
            for dlugosc_cena, ile in bilet.items():
                ile.set(0)
        self.wplacone.set(self.automat.suma_monet())
        self.do_zaplaty.set(self.automat.do_zaplaty())
        updateVar(self.wplacone, self.wplacone_string)
        updateVar(self.do_zaplaty, self.do_zaplaty_string)

    def zaplac(self):
        if self.do_zaplaty.get() > 0:
            wrzucone = self.automat._wrzucone.copy()
            bilety = self.automat._bilety.copy()
            zaplacone = self.automat.zaplac()

            if zaplacone == {}:
                tk_messagebox.showerror("Za mało gotówki!", "Wprowadzono niepełną kwotę!")
            else:
                if zaplacone == wrzucone:
                    tk_messagebox.showerror("Tylko odliczona kwota!",
                                            f'Tylko odliczona kwota!\nWrzucona gotówka:\n{self.automat.pokaz_monety(wrzucone)}\n')
                    self.zeruj_zakupy()

                elif zaplacone == {n: 0 for n in A.LISTA_NOMINALOW}:
                    zakupione = ''
                    for b in bilety:
                        zakupione += f'\n{b}'
                    tk_messagebox.showinfo("Zakupy pomyślne",
                                           f"Zakupione bilety:{zakupione}\nŁączna kwota: {self.do_zaplaty_string.get()}")
                    self.zeruj_zakupy()

                else:
                    zakupione = ''
                    for b in bilety:
                        zakupione += f'\n{b}'
                    tk_messagebox.showinfo("Zakupy pomyślne",
                                           f"Zakupione bilety:{zakupione}\nŁączna kwota: {self.do_zaplaty_string.get()}\nReszta:{self.automat.suma_monet(zaplacone) / 100:.2f}zł")
                    self.zeruj_zakupy()


        else:
            tk_messagebox.showwarning("Wybierz bilety!", "Proszę wybrać bilety do zakupu!")


t = tk.Tk()
t.title('Automat biletowy')
a = AutomatApplication(t, 100)
t.resizable(False, False)
t.update_idletasks()
width = t.winfo_width()
height = t.winfo_height()
x = (t.winfo_screenwidth() // 2) - (width // 2)
y = (t.winfo_screenheight() // 2) - (height // 2)
t.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# a.master.title('Automat biletowy')
a.mainloop()
