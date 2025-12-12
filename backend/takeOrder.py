from order import Order
from items import Item
from orderCheckout import OrderCheckout
from typing import Optional


class TakeOrder:
    """Manages the process of taking, modifying, and checking out customer orders."""

    def __init__(self, database=None):
        """
        Initialize TakeOrder.
        
        Args:
            database: Optional POSDatabase instance for persisting orders
        """
        # Stores the current active order, none if no order has started
        self.current_order = None

        # stores previously completed orders
        self.order_history = []
        
        # database connection (optional)
        self.database = database

    def start_new_order(self, order_id: int, customer_name: str = ""):
        """Creates a new order using the Order class."""
        if self.current_order is not None:
            raise ValueError("An order is already in progress. Please checkout or cancel the current order first.")
        
        self.current_order = Order(order_id, customer_name)

    def add_item_to_order(self, item: Item, quantity: int = 1):
        """Adds an item to the current order."""
        if self.current_order is None:
            raise ValueError("No active order. Start a new order first.")
        
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        
        self.current_order.add_item(item, quantity)

    def remove_item_from_order(self, item_id: int):
        """Removes an item from the current order by item ID."""
        if self.current_order is None:
            raise ValueError("No active order. Start a new order first.")
        
        self.current_order.remove_item(item_id)

    def checkout_order(self) -> float:
        """
        Uses OrderCheckout to calculate the total and finishes the order.
        If database is connected, saves the order to database.
        """
        if self.current_order is None:
            raise ValueError("No active order to checkout.")
        
        if len(self.current_order.item_list) == 0:
            raise ValueError("Cannot checkout an empty order.")
        
        # Calculate total using OrderCheckout
        checkout = OrderCheckout(self.current_order)
        total = checkout.calculate_total()
        
        # Save to database if available
        if self.database:
            db_order_id = self.database.save_order(self.current_order, total)
            if db_order_id:
                print(f"Order saved to database with ID: {db_order_id}")
        
        # Save order to history
        self.order_history.append(self.current_order)
        
        # Reset current order
        self.current_order = None
        
        return total

    def cancel_order(self):
        """Cancels the current order and resets it."""
        if self.current_order is None:
            raise ValueError("No active order to cancel.")
        
        self.current_order = None

    def get_current_order(self) -> Optional[Order]:
        """Returns the current active order."""
        return self.current_order
    
    def get_order_history(self) -> list:
        """Returns the list of all completed orders."""
        return self.order_history