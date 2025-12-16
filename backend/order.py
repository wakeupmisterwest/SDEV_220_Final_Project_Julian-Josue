from typing import List, Tuple
from items import Item


class Order:

    def __init__(self, orderID: int, customer_name: str = ""):
 
        # initializing an Order here
        self.orderID = orderID
        self.name = customer_name
        self.item_list = []          # list of item, quantity. tuples
        self.items_dict = {}         # dictionary, item_id.  item, quantity
    
    def add_item(self, item: Item, quantity: int = 1):

        # adds an item to the order
        if item.itemID in self.items_dict:
            existing_item, existing_qty = self.items_dict[item.itemID]
            self.items_dict[item.itemID] = (existing_item, existing_qty + quantity)
        else:
            self.items_dict[item.itemID] = (item, quantity)

        # rebuild list of tuples to keep rest of system working
        self.item_list = list(self.items_dict.values())
    
    def remove_item(self, item_id: int) -> None:
        #removes an Item from this order by item_id

        if item_id in self.items_dict:
            del self.items_dict[item_id]

        # rebuild list of tuples after removal
        self.item_list = list(self.items_dict.values())
    
    
    def get_items(self) -> list[tuple[Item, int]]:
            
            # this returns all items in this order
        return self.item_list
    
    def __str__(self):
         return (f"Order({self.orderID}, {self.name}, " f"Items: {len(self.item_list)})")
