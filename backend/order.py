from items import Item


class Order:

    def __init__(self, orderID: int, customer_name: str = ""):
 
        # initializing an Order here
        self.orderID = orderID
        self.name = customer_name
        self.item_list = []
    
    def add_item(self, item: Item, quantity: int = 1):

        # adds an item to the order
        self.item_list.append((item, quantity))
    
    def remove_item(self, item_id: int) -> None:
        #removes an Item from this order by item_id

        self.item_list = [(item, qty) for item, qty in self.item_list if item.itemID != item_id]
    
    
    def get_items(self) -> list[tuple[Item, int]]:
            
            # this returns all items in this order
        return self.item_list
    
    def __str__(self):
         return (f"Order({self.orderID}, {self.name}, " f"Items: {len(self.item_list)})")
