import tkinter as tk
import tkinter.font as tkFont
import Automat as A


class MyDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.resizable(False, False)

        self.coin_label = []
        self.coin_spinbox = []
        for c in A.LISTA_NOMINALOW:
            self.coin_label.append(tk.Label(top, text=f'{c / 100}zl'))
            self.coin_spinbox.append(
                tk.Spinbox(top, width=5, from_=0, to=100, state="readonly", bg='white', fg='black'))
        for i, coin in enumerate(zip(self.coin_spinbox, self.coin_label)):
            coin[1].grid(column=1, row=i, sticky=tk.N + tk.S + tk.E + tk.W)
            coin[0].grid(column=2, row=i, sticky=tk.N + tk.S + tk.E + tk.W)

        self.quitButton = tk.Button(top, text="Ok", command=lambda: self.ok())
        self.quitButton.grid(row=len(self.coin_spinbox), column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def ok(self):
        self.top.destroy()


def wrzuc_monety(master):
    d = MyDialog(master)
    master.wait_window(d.top)


def zaplac():
    print("Płacę")


class AutomatApplication(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.createWidgets()

    def createWidgets(self):
        top = self.winfo_toplevel()

        self.do_zaplaty = tk.DoubleVar(0.0)
        self.wplacone = tk.DoubleVar(0.0)

        self.do_zaplaty_desc_label = tk.Label(self, text="Kwota do zapłaty:", font=tkFont.Font(size=11), anchor='w')
        self.do_zaplaty_desc_label.grid(column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.wplacone_desc_label = tk.Label(self, text="Kwota wpłacona:", font=tkFont.Font(size=11), anchor='w')
        self.wplacone_desc_label.grid(column=0, row=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.do_zaplaty_label = tk.Label(self, textvariable=self.do_zaplaty)
        self.do_zaplaty_label.grid(column=1, row=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.wplacone_label = tk.Label(self, textvariable=self.wplacone)
        self.wplacone_label.grid(column=1, row=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.bilety_label = []
        self.bilety_spinbox = []
        for i, typ in enumerate(A.TYP_BILETU):
            self.bilety_label.append(
                [tk.Label(self, text=f'{bilet[0]}-minutowy {typ}\n{bilet[1] / 100 / (i + 1)}zł') for j, bilet
                 in enumerate(zip(A.DLUGOSC_BILETU_MINUTY, A.CENA_BILETU))])
            self.bilety_spinbox.append(
                [tk.Spinbox(self, from_=0, to=100, state="readonly", bg='white', fg='black') for j, bilet
                 in enumerate(zip(A.DLUGOSC_BILETU_MINUTY, A.CENA_BILETU))])

        for i, typ in enumerate(zip(self.bilety_label, self.bilety_spinbox)):
            for j, bilet in enumerate(zip(typ[0], typ[1])):
                bilet[1].grid(row=(5 + 2 * i), column=j, sticky=tk.N + tk.S + tk.E + tk.W)
                bilet[0].grid(row=(4 + 2 * i), column=j, sticky=tk.N + tk.S + tk.E + tk.W)

        tk.Label(self, text="Dostępne bilety:", font=tkFont.Font(size=13)).grid(row=3, column=0, columnspan=3)
        self.wrzuc_monety_button = tk.Button(self, text="Wrzuc monety", command=lambda: wrzuc_monety(self))
        self.wrzuc_monety_button.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.zaplac_button = tk.Button(self, text="Zapłać", command=lambda: zaplac())
        self.zaplac_button.grid(row=8, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.zakoncz_button = tk.Button(self, text="Zakończ", command=lambda: self.quit())
        self.zakoncz_button.grid(row=8, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
    # for i in range(len(self.coin_spinbox)):
    #     top.rowconfigure(i, weight=1)
    #     self.rowconfigure(i, weight=1)
    # top.columnconfigure(0, weight=1)
    # top.columnconfigure(1, weight=1)
    # top.columnconfigure(2, weight=1)
    # self.columnconfigure(0, weight=1)
    # self.columnconfigure(1, weight=1)
    # self.columnconfigure(2, weight=1)


t = tk.Tk()
t.title('Automat biletowy')
a = AutomatApplication(t)
t.resizable(False, False)
t.update_idletasks()
width = t.winfo_width()
height = t.winfo_height()
x = (t.winfo_screenwidth() // 2) - (width // 2)
y = (t.winfo_screenheight() // 2) - (height // 2)
t.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# a.master.title('Automat biletowy')
a.mainloop()
