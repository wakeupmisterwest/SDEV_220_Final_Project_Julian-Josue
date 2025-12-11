
#This is item Class and it Represents an individual item food or drink in the inventory

class Item:
    #Represents an individual item food or drink
    def __init__(self, item_ID: int, name: str, description: str, price: float):
   
        self.itemID = item_ID # stores the unique id for the item
        self.name = name    # this stores name of the item
        self.description = description  # this stores description about the items
        self.price = price # this stores price of the items
    
    def __str__(self):
        return f"Item({self.itemID}, {self.name}, ${self.price:.2f})"
    
    def __repr__(self):
        return self.__str__()
