from Data import DATASET

LINE: str = "-" * 50

class Ingredient:
    def __init__(self, quantity: int) -> None:
        self.quantity = quantity
        
    def CheckAvailable(self, amount: int) -> bool:
        return True if amount <= self.quantity else False
    
    def Consume(self, amount: int):
        self.quantity -= amount
        
class Coins:
    def CalculateChange(self, amount: float, price: float) -> list:
        coins: list[float] = [1.0, 0.5, 0.2, 0.1]
        amount = int(amount * 100)
        price = int(price * 100)
        
        change: int = amount - price
        changeSet: list[float] = []
        
        while change > 0 and change != 0:
            if change >= 100:
                change -= 100
                changeSet.append(coins[0])
            elif change >= 50:
                change -= 50
                changeSet.append(coins[1])
            elif change >= 20:
                change -= 20
                changeSet.append(coins[2])
            elif change >= 10:
                change -= 10
                changeSet.append(coins[3])
            else:
                pass
        
        return changeSet
        
class Coffee:
    def __init__(self, id: int) -> None:
        self.id: int = id
        detail: dict = DATASET[self.id]
        
        self.name: str = detail["name"]
        self.price: float = detail["price"]
        self.waterAmt: int = detail["process"][0]
        self.milkAmt: int = detail["process"][1]
        self.syrup: int = detail["process"][2]
        
    def DisplayDetails(self):
        print(f"Name     : {self.name}")
        print(f"Price    : {self.price}")
        
        
class Machine:
    def __init__(self) -> None:
        self.water = Ingredient(quantity = 2500)
        self.milk = Ingredient(quantity = 300)
        self.syrup = Ingredient(quantity = 1500)
        
        self.coins = Coins()
        
        self.orders: list[str] = []
        
        for idx in DATASET:
            self.orders.append(str(idx['id']))
        
        self.isOperating: bool = True
        self.adminComms: list[str] = ["report", "off"]
        
        self.GetInputs()
        
    def GetInputs(self):
        while self.isOperating:
            print(LINE)
            print("WELCOME TO COFFEE PALACE!!")
            print(LINE)
            print("What would you like to order?")
            for idx in DATASET:
                print(f"{idx['id']} : {idx['name']}")
            
            userIn = input(": ").lower()
            if userIn in self.adminComms:
                self.ControlPanel(command = userIn)
            
            elif userIn in self.orders:
                self.ProductOrder(int(userIn))
            
            else:
                print("\nERROR : Invalid Input!!\n")
            
        print(LINE)
        print(f"Machine Operating : {self.isOperating}")
        print(LINE)
            
    def ControlPanel(self, command: str):
        if command == "report":
            print(LINE)
            print(f"Machine Operating : {self.isOperating}")
            print(f"Water Quantity    : {self.water.quantity}")
            print(f"Milk Quantity     : {self.milk.quantity}")
            print(f"Syrup Quantity    : {self.syrup.quantity}")
        if command == "off":
            self.isOperating = False
            
    def ProductOrder(self, id: int):
        coffee = Coffee(id)
        canProcess: bool = False
        
        if coffee.waterAmt <= self.water.quantity:
            if coffee.milkAmt <= self.milk.quantity:
                if coffee.syrup <= self.syrup.quantity:
                    canProcess = True
        
        print(LINE)
        if canProcess is True:    
            coffee.DisplayDetails()
            print(LINE)
            print("Input Payment to Confirm Order (x) to Cancel : ")
            
            payAmount: list[float] = [0]
            confirmOrder: bool = True
            
            while sum(payAmount) < coffee.price and confirmOrder is True:
                print(f"Paid : {sum(payAmount)}")
                payIn = input("Insert Coins (1.0, 0.5, 0.2, 0.1) :").lower()
                if payIn == 'x':
                    confirmOrder = False
                    break
                elif payIn in ("1.0", "0.5", "0.2", "0.1"):
                    payAmount.append(float(payIn))
                else: pass
            
            if confirmOrder is True:
                print(LINE)
                payment: float = sum(payAmount)
                
                change = self.coins.CalculateChange(payment, coffee.price)
                print(f"Payment : $ {round(payment, 2)}")
                print(f"Price   : $ {round(coffee.price, 2)}")
                print(f"Change  : $ {round(sum(change), 2)}")
                print(f"Given   : {change}")
                
                self.water.Consume(coffee.waterAmt)
                self.milk.Consume(coffee.milkAmt)
                self.syrup.Consume(coffee.syrup)
                
                print(LINE)
                print("Thank You For Your Purchase!!\nEnjoy your Coffee!!")
            
        else:
            print("Sorry Product out of Stock!!")
        
            
machine = Machine()
