import interface
import logic


pepsi = logic.Item("Pepsi", 30, 3, 5)
mala_tania_woda = logic.Item("Mala tania woda", 47, 1, 5)
sok = logic.Item("Sok pomaranczowy", 48, 3.5, 5)
woda_gaz = logic.Item("Woda gazowana", 49, 2.5, 5)
woda_niegaz = logic.Item("Woda niegazowana", 50, 2, 5)
machine = logic.ItemStorage()
machine.add_item(pepsi)
machine.add_item(mala_tania_woda)
machine.add_item(sok)
machine.add_item(woda_gaz)
machine.add_item(woda_niegaz)
machine_coins = logic.CoinStorage()
machine_rest_coins = logic.CoinStorage()
machine_rest_coins.add_coin(logic.Coin(2))
machine_rest_coins.add_coin(logic.Coin(5))
display = interface.MachinePanel(machine, machine_coins, machine_rest_coins)
