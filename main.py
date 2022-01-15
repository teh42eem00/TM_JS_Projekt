from tkinter import *
from tkinter import ttk, messagebox
from decimal import *

possible_coins = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]


def unpack_dict(value, count):
    return value, count


def decimal_2places_rounded(value_before):
    return Decimal(round(value_before, 2))


def return_change(coins, to_return, coin_index=0):
    if to_return == 0:
        return []  # sukces gdy pozostalo 0 do zwrocenia
    if coin_index >= len(coins):
        return None  # nie udalo sie znalezc reszty
    coin = coins[coin_index]
    coin_index += 1
    # rozpoczynam od pobierania jak najwiekszej ilosci monet
    can_take = min(to_return // coin["value"], coin["count"])
    # pobieram monety az do osiagniecia kwoty 0
    for counter in range(can_take, -1, -1):  # odliczanie do 0
        # rekursywnie przechodze do kolejnych monet w celu dobrania odpowiednich kolejnych nominalow
        change = return_change(coins, to_return - coin["value"] * counter, coin_index)
        if change is not None:  # jezeli rekursywny przypadek nie zwrocil None
            if counter:  # i zostalo cos naliczone to dodaj do reszty
                return change + [{"value": coin["value"], "count": counter}]
            return change  # lub zwroc reszte


def flatten(nested_list):
    for item in nested_list:
        try:
            yield from flatten(item)
        except TypeError:
            yield item


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

    def add_multiple_coins(self, coin_value, coin_count):
        for ccount in range(coin_count):
            self.__coin_list.append(Coin(coin_value))

    def return_array_of_value(self):
        value_list = [float(o.get_value()) for o in self.__coin_list]
        return value_list

    def return_rest(self, rest_coin_value, rest_coin_count):
        rest_coin_txt = ""
        for rcount in range(rest_coin_count):
            selected_coin = next(
                (i for i, item in enumerate(self.__coin_list) if item.get_value() == rest_coin_value / 100), -1)
            rest_coin_txt = "Wydaje reszte o wartosci " + str(self.__coin_list.pop(selected_coin).get_value()) + "zl."
        return rest_coin_txt

    def return_coins(self):
        returned_coins_txt = ""
        while len(self.__coin_list):
            returned_coins_txt += "Zwracam monete o wartosci " + str(self.__coin_list.pop().get_value()) + " zl.\n"
        return returned_coins_txt

    def pop_coin_object(self):
        return self.__coin_list.pop()

    def return_len(self):
        return len(self.__coin_list)

    def take_money_inside(self, customer_money):
        while customer_money.return_len():
            self.__coin_list.append(customer_money.pop_coin_object())
        print(self.coin_sum())
        print(self.return_array_of_value())

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

    def get_item_price(self, chosen_item_number):
        if 50 >= chosen_item_number >= 30:
            selected_item = 0
            for index, item in enumerate(self.__item_list):
                if item.get_number() == chosen_item_number:
                    selected_item = index
            selected_item_price = self.__item_list[selected_item].get_price()
            return selected_item_price
        else:
            print("Blad!")

    def buy_item(self, chosen_item_number, money_placed):
        selected_item_price = self.get_item_price(chosen_item_number)
        if money_placed >= selected_item_price:
            rest = money_placed - selected_item_price
            print("Obliczona reszta do wydania: ", rest)
            if rest == 0:
                messagebox.showinfo("Sukces", "Zakup produktu o numerze " + str(chosen_item_number) + " udany")
                machine_rest_coins.take_money_inside(machine_coins)
            else:
                rest_available_coins = machine_rest_coins.return_array_of_value()  # lista wartosci
                rest_available_coins = [int(i * 100) for i in rest_available_coins]
                counted_rest_coins = {}  # slownik przechowujacy monety w formie {wartosc , ilosc}
                for r in rest_available_coins:  # zliczenie ilosci monet dostepnych do wydania reszty
                    counted_rest_coins[r] = counted_rest_coins.get(r, 0) + 1
                counted_rest_coins_list = list()  # lista przechowujaca slowniki zliczonych monet
                for key, (d_value, d_count) in enumerate(counted_rest_coins.items()):  # dodanie slownikow do listy
                    d = {"value": d_value, "count": d_count}
                    counted_rest_coins_list.append(d)
                returned_change_dict_list = return_change(counted_rest_coins_list, int(rest * 100))  # obliczenie reszty
                if returned_change_dict_list is None:  # jezeli nie udalo sie obliczyc reszty zwroc blad
                    messagebox.showinfo("Brak monet!", "Nie mozna wydac reszty, zakup anulowany!")
                    messagebox.showinfo("Zwrot monet", machine_coins.return_coins())
                else:  # w przeciwnym razie pobierz pieniadze i wydaj reszte
                    print(returned_change_dict_list)
                    for rc in returned_change_dict_list:  # dla wszystkich slownikow reszty (nominal, ilosc)
                        print(
                            machine_rest_coins.return_rest(*unpack_dict(**rc)))  # zwroc reszte z rozpakowanego slownika
                        messagebox.showinfo("Sukces", "Zakup produktu o numerze " + str(chosen_item_number) + " udany")
                        machine_rest_coins.take_money_inside(machine_coins)


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
        self._mainframe.grid(column=0, row=0)
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
        ttk.Button(self._mainframe, text="Przerwij", command=lambda: self.action_on_cancel()).grid(column=0, row=5)
        ttk.Button(self._mainframe, text="Monety - Reszta",
                   command=lambda: print(machine_rest_coins.return_array_of_value())).grid(column=0, row=6)
        ttk.Button(self._mainframe, text="Monety - Wplacone",
                   command=lambda: print(machine_coins.return_array_of_value())).grid(column=0, row=7)
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
                if machine_coins.coin_sum() < machine.get_item_price(int(self._buyers_choice)):
                    messagebox.showinfo("Za mało!",
                                        "Produkt kosztuje " + str(machine.get_item_price(int(self._buyers_choice))))
                else:
                    self._money_amount.set("")
                    machine.buy_item(int(self._buyers_choice), machine_coins.coin_sum())
            else:
                messagebox.showinfo("Blad", "Bledny numer produktu!")

    def action_on_money(self, money):
        machine_coins.add_coin(Coin(money))
        self._money_amount.set(str(machine_coins.coin_sum()))

    def action_on_cancel(self):
        messagebox.showinfo("Zwrot monet", machine_coins.return_coins())
        self._money_amount.set("")


pepsi = Item("Pepsi", 30, 3, 5)
mala_tania_woda = Item("Mala tania woda", 47, 1, 5)
sok = Item("Sok pomaranczowy", 48, 3.5, 5)
woda_gaz = Item("Woda gazowana", 49, 2.5, 5)
woda_niegaz = Item("Woda niegazowana", 50, 2, 5)
machine = ItemStorage()
machine.add_item(pepsi)
machine.add_item(mala_tania_woda)
machine.add_item(sok)
machine.add_item(woda_gaz)
machine.add_item(woda_niegaz)
machine_coins = CoinStorage()
machine_rest_coins = CoinStorage()
machine_rest_coins.add_coin(Coin(2))
machine_rest_coins.add_coin(Coin(5))
display = MachinePanel()
