from order import Order
from items import Item

class OrderCheckout:
    # Handles the calculation of the total for a given Order.

    def __init__(self, order: Order):

      #  Constructor that receives an Order object and stores it.
        self.order = order    # Store the order so we can access its items

    def calculate_total(self) -> float:

        #Calculates the total cost of the order by summing item price * quantity for each item in the order.

        total = 0.0   # total starts at 0

        # this is loop through each item and quantity pair in the order
        for item, quantity in self.order.item_list:

        # price of item multiplied by how many were ordered
            total += item.price * quantity

        tax_rate = 0.07
        tax = total * tax_rate
        total += tax

        # Return the final total
        return round(total, 2)

    def __str__(self):

        total = self.calculate_total()
        return f"OrderCheckout(Total: ${total:.2f})"
