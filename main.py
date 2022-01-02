from tkinter import *
from tkinter import ttk
from decimal import *

possible_coins = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]


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
            else:
                print("Za malo srodkow, produkt kosztuje " + str(selected_item_price))


# class BuyersChoice:
#     def __init__(self):
#         self.__choice = 0
#
#     def get_choice(self):
#         return self.__choice
#
#     def check_digits(self):
#         return len(str(self.__choice))
#
#     def add_digit(self, sent_digit):
#         if len(str(self.__choice)) == 0 or self.__choice == 0:
#             self.__choice = int(str(sent_digit))
#         elif (len(str(self.__choice))) == 1:
#             self.__choice = int(str(self.__choice) + str(sent_digit))


class MachinePanel:
    def __init__(self):
        # Tworzenie okna
        self._window = Tk()
        self._window.title("Automat")
        self._money_amount = StringVar()
        self._item_choice = StringVar()
        self._buyers_choice = ""
        # Tworzenie siatki na przyciski
        self._mainframe = ttk.Frame(self._window)
        # Umieszczenie siatki w oknie
        self._mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        # Dodanie przycisków do wrzucania monet
        self._i = 0
        for coin in possible_coins:
            ttk.Button(self._mainframe, text="Wrzuć " + str(coin) + "zł",
                       command=lambda lcoin=coin: self.action_on_money(lcoin)).grid(column=4, row=self._i)
            self._i += 1
        [ttk.Button(self._mainframe, text=str(digit + 1),
                    command=lambda ldigit=digit: self.action_on_choice(ldigit + 1)).grid(row=digit // 3 + 2,
                                                                                         column=digit % 3) for digit
         in range(9)]
        ttk.Button(self._mainframe, text="0", command=lambda: self.action_on_choice(0)).grid(row=5, column=1)
        # Dodanie przycisku sprawdzenia wartości zawartości
        ttk.Button(self._mainframe, text="Przerwij", command=lambda: machine_coins.return_coins()).grid(column=0, row=5)
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
            machine.buy_item(int(self._buyers_choice), machine_coins.coin_sum())

    def action_on_money(self, money):
        machine_coins.add_coin(Coin(money))
        self._money_amount.set(machine_coins.coin_sum())


pepsi = Item("Pepsi", 30, 3.50, 5)
machine = ItemStorage()
machine.add_item(pepsi)
machine_coins = CoinStorage()
display = MachinePanel()
