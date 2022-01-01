from tkinter import *
from tkinter import ttk
from decimal import *

possible_coins = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
input_panel = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]


def decimal_2places_rounded(value_before):
    return Decimal(round(value_before, 2))


class Coin:
    def __init__(self, value):
        if value in possible_coins:
            self.__value = decimal_2places_rounded(value)
        else:
            self.__value = 0

    def get_value(self):
        return decimal_2places_rounded(self.__value)


class CoinStorage:
    def __init__(self):
        self.__coin_list = []

    def add_coin(self, added_coin):
        if isinstance(added_coin, Coin):
            self.__coin_list.append(added_coin)
        else:
            print("Przeslany obiekt nie jest moneta!")

    def return_coins(self):
        while len(self.__coin_list):
            print("Zwracam monete o wartosci " + str(self.__coin_list.pop().get_value()) + " zl.")

    def coin_sum(self):
        counted_coins = 0
        for obj in self.__coin_list:
            counted_coins += obj.get_value()
        return counted_coins


class Item:
    def __init__(self, name, number, price, count):
        self._name = name
        self._number = number
        self._price = decimal_2places_rounded(price)
        self._count = count

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_number(self):
        return self._number

    def set_number(self, number):
        self._number = number

    def get_price(self):
        return decimal_2places_rounded(self._price)

    def set_price(self, price):
        self._price = price

    def get_count(self):
        return self._count

    def set_count(self, count):
        self._count = count

    def string_name_price(self):
        return str(self._number) + ". Nazwa: " + str(self._name) + " Cena: " + str(self._price)


class ItemStorage:
    def __init__(self):
        self.__item_list = []

    def add_item(self, added_item):
        if isinstance(added_item, Item):
            self.__item_list.append(added_item)
        else:
            print("Przeslany obiekt nie jest przedmiotem!")

    def buy_item(self, chosen_item_number, money_placed):
        if 50 >= chosen_item_number >= 30:
            selected_item = next(
                (i for i, item in enumerate(self.__item_list) if item.get_number() == chosen_item_number), -1)
            selected_item_name = self.__item_list[selected_item].get_name()
            selected_item_price = self.__item_list[selected_item].get_price()
            if money_placed >= selected_item_price:
                print("Zakup " + selected_item_name + " udany")
                print("Wydaje reszte " + str(money_placed - selected_item_price))


class BuyersChoice:
    def __init__(self):
        self.__choice = 0

    def get_choice(self):
        return self.__choice

    def check_digits(self):
        return len(str(self.__choice))

    def add_digit(self, sent_digit):
        if len(str(self.__choice)) == 0 or self.__choice == 0:
            self.__choice = int(str(sent_digit))
        elif (len(str(self.__choice))) == 1:
            self.__choice = int(str(self.__choice) + str(sent_digit))


pepsi = Item("Pepsi", 30, 3.50, 5)
buyers_choice = BuyersChoice()
machine = ItemStorage()
machine.add_item(pepsi)
machine_coins = CoinStorage()
# Tworzenie okna
window = Tk()
window.title("Automat")
# Tworzenie siatki na przyciski
mainframe = ttk.Frame(window)
# Umieszczenie siatki w oknie
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# Dodanie przycisków do wrzucania monet
i = 0
chosen_product = 0
for coin in possible_coins:
    ttk.Button(mainframe, text="Wrzuć " + str(coin) + "zł",
               command=lambda coin=coin: machine_coins.add_coin(Coin(coin))).grid(column=2, row=i)
    i += 1
for input_button in input_panel:
    ttk.Button(mainframe, text=str(input_button),
               command=lambda input_button=input_button: buyers_choice.add_digit(input_button)).grid(
        column=3, row=input_button)
# Dodanie przycisku sprawdzenia wartości zawartości
ttk.Button(mainframe, text="Przerwij", command=lambda: print(machine_coins.coin_sum())).grid(column=1, row=0)
ttk.Button(mainframe, text="Zwroc", command=lambda: machine_coins.return_coins()).grid(column=1, row=1)
ttk.Button(mainframe, text="Zakup",
           command=lambda: machine.buy_item(buyers_choice.get_choice(), machine_coins.coin_sum())).grid(column=1,
                                                                                                        row=2)
ttk.Button(mainframe, text="Zamowienie", command=lambda: print(buyers_choice.get_choice())).grid(column=1, row=3)
window.mainloop()
