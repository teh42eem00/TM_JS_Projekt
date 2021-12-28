from tkinter import *
from tkinter import ttk
from decimal import *

possible_coins = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]


def rounded_coin(value_before):
    return Decimal(round(value_before, 2))


class Coin:
    def __init__(self, value):
        if value in possible_coins:
            self.__value = rounded_coin(value)
        else:
            self.__value = 0

    def get_value(self):
        return rounded_coin(self.__value)


class CoinStorage:
    def __init__(self):
        self.__coin_list = []

    def add_coin(self, added_coin):
        if isinstance(added_coin, Coin):
            self.__coin_list.append(added_coin)
        else:
            print("Przeslany obiekt nie jest moneta!")

    def coin_sum(self):
        counted_coins = 0
        for obj in self.__coin_list:
            counted_coins += obj.get_value()
        return counted_coins


class Item:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = price

    def string_name_price(self):
        return "Nazwa: " + str(self._name) + " Cena: " + str(self._price)


pb = CoinStorage()
# Tworzenie okna
window = Tk()
window.title("Automat")
# Tworzenie siatki na przyciski
mainframe = ttk.Frame(window)
# Umieszczenie siatki w oknie
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# Dodanie przycisków do wrzucania monet
i = 0
for coin in possible_coins:
    ttk.Button(mainframe, text="Wrzuć " + str(coin) + "zł",
               command=lambda coin=coin: pb.add_coin(Coin(coin))).grid(column=2, row=i)
    i += 1
# Dodanie przycisku sprawdzenia wartości zawartości
ttk.Button(mainframe, text="Przerwij", command=lambda: print(pb.coin_sum())).grid(column=1, row=0)
window.mainloop()
