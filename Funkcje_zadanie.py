import time

def SetItemsValues(Amount, Weight, Value):
    return {
        "Ilosc" : Amount,
        "Waga" : Weight,
        "Wartosc" : Value
    }

def SetStarterInventory():
    inventory = {
        'miecz': SetItemsValues(1, 5, 30),
        'mikstura': SetItemsValues(3, 2, 10),
        "zloto": SetItemsValues(50, 1, 1)
    }

    return inventory

def GetInventory(CurrentInventory):
    inventoryToReturn = CurrentInventory

    if not inventoryToReturn:
        inventoryToReturn = SetStarterInventory()

    return inventoryToReturn

def AddItem(CurrentInventory, MinToAdd):
    KeyWord = MinToAdd > 0 and "zwiekszyc lub kompletnie dodac: " or "zmiejszyc: "
    KeyWord2 = MinToAdd > 0 and "Pomyslnie dodano item" or "Pomyslnie usnieto item"
    KeyWord3 = MinToAdd > 0 and "dodac" or "usunac"
    correction = MinToAdd > 0 and 1 or -1

    print("")
    ItemToAdd = input(f"Podaj nazwe przemiotu który chcesz {KeyWord}")

    #Item juz istnieje dodaj go
    if ItemToAdd in CurrentInventory:
        AmountToAdd = abs(int(input(f"Podaj ile chcesz {KeyWord3} {ItemToAdd} (0 by anluzowac): ")))
        AmountToAdd = max(AmountToAdd, 0) #pilnuj aby nigdy nie spadlo ponizej zera (aby user nie mogl sprzedac -1)
        
        if MinToAdd < 1 and AmountToAdd > CurrentInventory[ItemToAdd]["Ilosc"]:
            AmountToAdd = min(AmountToAdd, CurrentInventory[ItemToAdd]["Ilosc"])
            print(f"\nWpisałes wiecej {ItemToAdd} niz miales\nograniczono liczbe sprzedazy do {AmountToAdd}\n")
        
        #W tej sekcji usun/dodaj zloto (To juz nie jest zwykle zloto...)
        PatternForMoney = (CurrentInventory[ItemToAdd]['Wartosc'] * AmountToAdd) * MinToAdd 
        if CurrentInventory['zloto']['Ilosc'] >= PatternForMoney: 
            CurrentInventory['zloto']['Ilosc'] += PatternForMoney * (-1)
            CurrentInventory[ItemToAdd]['Ilosc'] += AmountToAdd * correction
            print(KeyWord2, ItemToAdd) #wazny print nie usun mi go przypadkiem idioto
        else:
            print("Nie masz wystarczjaco pieniedzy aby kupic", AmountToAdd, "sztuki", ItemToAdd, "brakuje ci", PatternForMoney-CurrentInventory['zloto']['Ilosc'] )
        
        MaxAmount = ItemToAdd == "zloto" and 50 or 20 #zrobił bym to zmiennymi globalnymi MAX_FOR_ITEMS = 20 jak by co w taki sposób ale nie mozna globalnych 
        
        #UWAGA DO PANA: tu przy wklejaniu się czasem psuje jeśli pan wkleja kod więc tutaj IFy 2 kolejne sa zagniezdzone (bez elsea)
        if CurrentInventory[ItemToAdd]['Ilosc'] > MaxAmount:
            CurrentInventory[ItemToAdd]['Ilosc'] = MaxAmount
            print("Nie możesz mieć więcej niż",MaxAmount,"sztuki przedmiotu",ItemToAdd)

        if CurrentInventory[ItemToAdd]["Ilosc"] < 1 and ItemToAdd != "zloto":
            CurrentInventory.pop(ItemToAdd)
            print("Pozbyto sie wszystkich przedmiotow o nazwie", ItemToAdd)
    #Item jeszcze nie istnieje (dodanie)
    elif MinToAdd > 0:
        AmountToAdd = int(input("Podaj ile chcesz dodac tych itemow: "))
        AmountToAdd = max(AmountToAdd, MinToAdd)
        WeightOfItem = int(input("Podaj ile przedmiot ma wazyc: "))
        ValueOfItem = int(input("Podaj wartosc itemu (uwaga wartosc * Value musi byc wieksze od ilosci zlota): "))
        
        if AmountToAdd * ValueOfItem > CurrentInventory["zloto"]["Ilosc"]:
            print("Nie masz wystarczajaco zlota na ",AmountToAdd,"sztuk po ",ValueOfItem, "zlota")
            print("Twoje zloto to ", CurrentInventory["zloto"]["Ilosc"])
            print("Sorry, nie stac Cię 😔")
        else: 
            CurrentInventory[ItemToAdd] = SetItemsValues(AmountToAdd, WeightOfItem, ValueOfItem)
            CurrentInventory["zloto"]["Ilosc"] -= AmountToAdd * ValueOfItem
    else:
        print("Nie masz itemu", ItemToAdd, "wiec nie mozesz go usunac")

def CheckForItem(CurrentInventory):
    ItemToCheck = input("Podaj item którego szukasz: ")
    print("")
    if ItemToCheck in CurrentInventory:
        print("Masz", CurrentInventory[ItemToCheck],"X",ItemToCheck)
    else:
        print("Nie posiadasz itemu o nazwie ", ItemToCheck)

def PrintInventory(InventoryToPrint):
    Choise = input("Czy chcesz dokladnie zobaczyc (d) czy tylko itemy (i, nic): ").lower()
    FullScan = Choise == "d" and True or False
    
    print("\nTwoj ekwipunek: ")
    
    for item, value in InventoryToPrint.items():
        print("-", item)
        
        if not FullScan:
            continue
        
        for component, compValue in value.items():
            print("  -", component, ":", compValue)
        print("")
        time.sleep(0.5)

def PrintMenu():
    print("Menu: ")
    print("1. Pokaż przedmioty (dokładniej)")
    print("2. Dodaj Przedmiot")
    print("3. Użyj przedmiotu (sprzedaj)")
    print("4. Sprawdz przedmiot")
    print("5. Wyjdz")

def GameRound(GivenInventory):
    CurrentInventory = GetInventory(GivenInventory)

    PrintMenu()

    print("\nTwoj ekwipunek: ", CurrentInventory)
    usersChoice = input("Twoj wybor: ")
    
    if usersChoice == "1":
        PrintInventory(CurrentInventory)
    elif usersChoice == "2":
        AddItem(CurrentInventory, 1)
    elif usersChoice == "3":
        AddItem(CurrentInventory, -1)
    elif usersChoice == "4":
        CheckForItem(CurrentInventory)
    elif usersChoice == "5":
        print("Wychodze...")
        return

    #zawsze na koncu lekki odstep
    time.sleep(1)
    print("")
    GameRound(CurrentInventory)

GameRound({})