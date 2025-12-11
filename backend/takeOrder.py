from order import Order
from items import Item
from orderCheckout import OrderCheckout

class TakeOrder:

    def __init__(self):
        # Stores the current active order, none if no order has started
        self.current_order = None

        # stores previously completed orders, this is optional
        self.order_history = []

    def start_new_order(self, order_id: int, customer_name: str = ""):   #  Creates a new order using the Order class.

        #Working on logic
        pass

    def add_item_to_order(self, item: Item, quantity: int = 1):  # adds an item to the current order.

        #Working on logic
        pass

    def remove_item_from_order(self, item_id: int):  # Removes an item from the current order by item ID.

        # Working on logic
        self.current_order.remove_item(item_id)
        pass

    def checkout_order(self) -> float:   #Uses OrderCheckout to calculate the total and finishes the order.

        # Working on logic

        pass

    def cancel_order(self):   #cancels the current order and resets it.

        # Working on logic
        pass
