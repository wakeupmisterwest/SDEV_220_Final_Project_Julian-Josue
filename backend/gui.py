import tkinter as tk
from tkinter import messagebox


class Item:
    """Represents an individual food or drink item in the inventory."""

    def __init__(self, item_id: int, name: str, description: str, price: float):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = price

    def __str__(self) -> str:
        return f"Item({self.item_id}, {self.name}, ${self.price:.2f})"

    def __repr__(self) -> str:
        return f"Item(item_id={self.item_id}, name={self.name!r}, price={self.price})"


class Order:
    """Represents a customer order containing items and their quantities."""

    def __init__(self, order_id: int, customer_name: str = ""):
        self.order_id = order_id
        self.name = customer_name
        self.item_list: list[tuple[Item, int]] = []

    def add_item(self, item: Item, quantity: int = 1) -> None:
        self.item_list.append((item, quantity))

    def remove_item(self, item_id: int) -> None:
        self.item_list = [(item, qty) for item, qty in self.item_list if item.item_id != item_id]

    def get_items(self) -> list[tuple[Item, int]]:
        return self.item_list

    def __str__(self) -> str:
        return f"Order({self.order_id}, {self.name}, Items: {len(self.item_list)})"


class OrderCheckout:
    """Handles the calculation of the total for a given Order."""

    def __init__(self, order: Order) -> None:
        self.order = order

    def calculate_total(self) -> float:
        total = 0.0
        for item, quantity in self.order.item_list:
            total += item.price * quantity
        return total

    def __str__(self) -> str:
        total = self.calculate_total()
        return f"OrderCheckout(Total: ${total:.2f})"


class TakeOrder:
    """Manages the process of taking, modifying, and checking out customer orders."""

    def __init__(self):
        self.current_order: Order | None = None
        self.order_history: list[Order] = []

    def start_new_order(self, order_id: int, customer_name: str = "") -> None:
        self.current_order = Order(order_id, customer_name)

    def add_item_to_order(self, item: Item, quantity: int = 1) -> None:
        if self.current_order is None:
            raise ValueError("No active order. Start a new order first.")
        self.current_order.add_item(item, quantity)

    def remove_item_from_order(self, item_id: int) -> None:
        if self.current_order is None:
            raise ValueError("No active order. Start a new order first.")
        self.current_order.remove_item(item_id)

    def checkout_order(self) -> float:
        if self.current_order is None:
            raise ValueError("No active order to checkout.")
        checkout = OrderCheckout(self.current_order)
        total = checkout.calculate_total()
        self.order_history.append(self.current_order)
        self.current_order = None
        return total

    def cancel_order(self) -> None:
        self.current_order = None


class OrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Ordering System")

        self.take_order = TakeOrder()

        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        self.middle_frame = tk.Frame(root)
        self.middle_frame.pack(pady=10)

        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(pady=10)

        tk.Label(self.top_frame, text="Order ID:").grid(row=0, column=0)
        self.order_id_entry = tk.Entry(self.top_frame)
        self.order_id_entry.grid(row=0, column=1)

        tk.Label(self.top_frame, text="Customer Name:").grid(row=1, column=0)
        self.customer_name_entry = tk.Entry(self.top_frame)
        self.customer_name_entry.grid(row=1, column=1)

        tk.Button(self.top_frame, text="Start New Order", command=self.start_order).grid(row=2, columnspan=2, pady=5)

        tk.Label(self.middle_frame, text="Item ID:").grid(row=0, column=0)
        self.item_id_entry = tk.Entry(self.middle_frame)
        self.item_id_entry.grid(row=0, column=1)

        tk.Label(self.middle_frame, text="Item Name:").grid(row=1, column=0)
        self.item_name_entry = tk.Entry(self.middle_frame)
        self.item_name_entry.grid(row=1, column=1)

        tk.Label(self.middle_frame, text="Description:").grid(row=2, column=0)
        self.item_desc_entry = tk.Entry(self.middle_frame)
        self.item_desc_entry.grid(row=2, column=1)

        tk.Label(self.middle_frame, text="Price:").grid(row=3, column=0)
        self.item_price_entry = tk.Entry(self.middle_frame)
        self.item_price_entry.grid(row=3, column=1)

        tk.Label(self.middle_frame, text="Quantity:").grid(row=4, column=0)
        self.item_qty_entry = tk.Entry(self.middle_frame)
        self.item_qty_entry.grid(row=4, column=1)

        tk.Button(self.middle_frame, text="Add Item", command=self.add_item).grid(row=5, columnspan=2, pady=5)

        tk.Button(self.bottom_frame, text="Remove Item", command=self.remove_item).grid(row=0, column=0, padx=5)
        tk.Button(self.bottom_frame, text="Checkout", command=self.checkout).grid(row=0, column=1, padx=5)
        tk.Button(self.bottom_frame, text="Cancel Order", command=self.cancel_order).grid(row=0, column=2, padx=5)

        self.display = tk.Text(root, height=10, width=50)
        self.display.pack(pady=10)

    def start_order(self):
        try:
            order_id = int(self.order_id_entry.get())
            customer_name = self.customer_name_entry.get()
            self.take_order.start_new_order(order_id, customer_name)
            self.display_message(f"Started new order {order_id} for {customer_name}")
        except ValueError:
            messagebox.showerror("Error", "Order ID must be an integer.")

    def add_item(self):
        try:
            item_id = int(self.item_id_entry.get())
            name = self.item_name_entry.get()
            desc = self.item_desc_entry.get()
            price = float(self.item_price_entry.get())
            qty = int(self.item_qty_entry.get())

            item = Item(item_id, name, desc, price)
            self.take_order.add_item_to_order(item, qty)
            self.display_message(f"Added {qty} x {name} (${price:.2f})")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for item fields.")

    def remove_item(self):
        try:
            item_id = int(self.item_id_entry.get())
            self.take_order.remove_item_from_order(item_id)
            self.display_message(f"Removed item with ID {item_id}")
        except ValueError:
            messagebox.showerror("Error", "Item ID must be an integer.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def checkout(self):
        try:
            total = self.take_order.checkout_order()
            self.display_message(f"Order checked out. Total = ${total:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_order(self):
        self.take_order.cancel_order()
        self.display_message("Order cancelled.")

    def display_message(self, msg: str):
        self.display.insert(tk.END, msg + "\n")
        self.display.see(tk.END)


root = tk.Tk()
app = OrderApp(root)
root.mainloop()