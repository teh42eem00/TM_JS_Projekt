from tkinter import *
from tkinter import ttk, messagebox
import logic

possible_coins = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]


class MachinePanel:
    def __init__(self, machine_items, machine_coins_input, machine_coins_change):
        # Tworzenie okna
        self._machine_items = machine_items
        self._machine_coins_input = machine_coins_input
        self._machine_coins_change = machine_coins_change
        self._window = Tk()
        self._window.title("Automat")
        self._money_amount = StringVar()
        self._item_choice = StringVar()
        self._buyers_choice = ""
        # Tworzenie siatki na przyciski
        self._mainframe = ttk.Frame(self._window)
        # Umieszczenie siatki w oknie
        self._mainframe.grid(column=0, row=0)
        # Dodanie przycisków do wrzucania monet
        self._i = 0
        for coin in possible_coins:
            ttk.Button(self._mainframe, text="Wrzuć " + str(coin) + "zł",
                       command=lambda lcoin=coin: self.action_on_money(lcoin)).grid(column=4, row=self._i)
            self._i += 1
        [ttk.Button(self._mainframe, text=str(digit + 1),
                    command=lambda ldigit=digit: self.action_on_choice(ldigit + 1)).grid(row=digit // 3 + 2,
                                                                                         column=digit % 3) for digit in
         range(9)]
        ttk.Button(self._mainframe, text="0", command=lambda: self.action_on_choice(0)).grid(row=5, column=1)
        # Dodanie przycisku sprawdzenia wartości zawartości
        ttk.Button(self._mainframe, text="Przerwij", command=lambda: self.action_on_cancel()).grid(column=0, row=5)
        ttk.Button(self._mainframe, text="Monety - Reszta",
                   command=lambda: print(self._machine_coins_change.return_array_of_value())).grid(column=0, row=6)
        ttk.Button(self._mainframe, text="Monety - Wplacone",
                   command=lambda: print(self._machine_coins_input.return_array_of_value())).grid(column=0, row=7)
        ttk.Label(self._mainframe, textvariable=self._money_amount).grid(column=0, row=0)
        ttk.Label(self._mainframe, textvariable=self._item_choice).grid(column=0, row=1)
        self._window.mainloop()

    def action_on_choice(self, choice):
        choice = str(choice)
        if len(self._buyers_choice) == 0 or len(self._buyers_choice) == 2:
            self._buyers_choice = choice
            self._item_choice.set(self._buyers_choice)
        elif len(self._buyers_choice) == 1:
            self._buyers_choice += choice
            self._item_choice.set(self._buyers_choice)
            if 50 >= int(self._buyers_choice) >= 30:
                if self._machine_coins_input.coin_sum() < self._machine_items.get_item_price(int(self._buyers_choice)):
                    messagebox.showinfo("Za mało!",
                                        "Produkt kosztuje " + str(
                                            self._machine_items.get_item_price(int(self._buyers_choice))))
                else:
                    self._money_amount.set("")
                    buy_status, buy_message = (
                        self._machine_items.buy_item(int(self._buyers_choice), self._machine_coins_input.coin_sum(),
                                                     self._machine_coins_change, self._machine_coins_input))
                    messagebox.showinfo(buy_status, buy_message)
            else:
                messagebox.showinfo("Blad", "Bledny numer produktu!")

    def action_on_money(self, money):
        self._machine_coins_input.add_coin(logic.Coin(money))
        self._money_amount.set(str(self._machine_coins_input.coin_sum()))

    def action_on_cancel(self):
        messagebox.showinfo("Zwrot monet", self._machine_coins_input.return_coins())
        self._money_amount.set("")
