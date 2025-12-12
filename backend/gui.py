import tkinter as tk
from tkinter import messagebox
from database import POSDatabase
from orderCheckout import OrderCheckout
from takeOrder import TakeOrder
from items import Item
from order import Order
import add_menu_items

'''
class Item:
    """Represents an individual food or drink item in the inventory."""

    def __init__(self, item_id: int, name: str, description: str, price: float):
        self.itemID = item_id
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
'''

class OrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Ordering System")

        # Initialize database
        self.db = POSDatabase("restaurant.db")
        self.take_order = TakeOrder()
        
        # Get next order ID
        self.next_order_id = self.get_next_order_id()

        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        self.middle_frame = tk.Frame(root)
        self.middle_frame.pack(pady=10)

        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(pady=10)

        # Order ID (auto-filled, read-only)
        tk.Label(self.top_frame, text="Order ID:").grid(row=0, column=0)
        self.order_id_entry = tk.Entry(self.top_frame, state='readonly')
        self.order_id_entry.grid(row=0, column=1)

        tk.Label(self.top_frame, text="Customer Name:").grid(row=1, column=0)
        self.customer_name_entry = tk.Entry(self.top_frame)
        self.customer_name_entry.grid(row=1, column=1)

        tk.Button(self.top_frame, text="Start New Order", command=self.start_order).grid(row=2, columnspan=2, pady=5)

        # Item ID with lookup
        tk.Label(self.middle_frame, text="Item ID:").grid(row=0, column=0)
        self.item_id_entry = tk.Entry(self.middle_frame)
        self.item_id_entry.grid(row=0, column=1)
        self.item_id_entry.bind('<Return>', self.lookup_item)  # Lookup on Enter key
        self.item_id_entry.bind('<FocusOut>', self.lookup_item)  # Lookup on tab/click away
        
        tk.Button(self.middle_frame, text="🔍", command=self.lookup_item, width=3).grid(row=0, column=2)

        tk.Label(self.middle_frame, text="Item Name:").grid(row=1, column=0)
        self.item_name_entry = tk.Entry(self.middle_frame)
        self.item_name_entry.grid(row=1, column=1, columnspan=2, sticky='ew')

        tk.Label(self.middle_frame, text="Description:").grid(row=2, column=0)
        self.item_desc_entry = tk.Entry(self.middle_frame)
        self.item_desc_entry.grid(row=2, column=1, columnspan=2, sticky='ew')

        tk.Label(self.middle_frame, text="Price:").grid(row=3, column=0)
        self.item_price_entry = tk.Entry(self.middle_frame)
        self.item_price_entry.grid(row=3, column=1, columnspan=2, sticky='ew')

        tk.Label(self.middle_frame, text="Quantity:").grid(row=4, column=0)
        self.item_qty_entry = tk.Entry(self.middle_frame)
        self.item_qty_entry.grid(row=4, column=1, columnspan=2, sticky='ew')

        tk.Button(self.middle_frame, text="Add Item", command=self.add_item).grid(row=5, columnspan=3, pady=5)

        tk.Button(self.bottom_frame, text="Remove Item", command=self.remove_item).grid(row=0, column=0, padx=5)
        tk.Button(self.bottom_frame, text="Checkout", command=self.checkout).grid(row=0, column=1, padx=5)
        tk.Button(self.bottom_frame, text="Cancel Order", command=self.cancel_order).grid(row=0, column=2, padx=5)

        self.display = tk.Text(root, height=10, width=50, state='disabled')
        self.display.pack(pady=10)
        
        # Set initial order ID
        self.update_order_id_display()

    def get_next_order_id(self):
        """Get the next available order ID"""
        orders = self.db.get_all_orders(limit=1)
        if orders:
            return orders[0]['order_id'] + 1
        return 1

    def update_order_id_display(self):
        """Update the order ID field"""
        self.order_id_entry.config(state='normal')
        self.order_id_entry.delete(0, tk.END)
        self.order_id_entry.insert(0, str(self.next_order_id))
        self.order_id_entry.config(state='readonly')

    def lookup_item(self, event=None):
        """Look up item from database by ID"""
        try:
            item_id_str = self.item_id_entry.get().strip()
            if not item_id_str:
                return
            
            item_id = int(item_id_str)
            
            # Prevent duplicate lookups for the same item
            if hasattr(self, '_last_lookup_id') and self._last_lookup_id == item_id:
                return
            
            self._last_lookup_id = item_id
            
            # If ID is 0, enable manual entry
            if item_id == 0:
                self.clear_item_fields()
                self.enable_item_fields()
                self.display_message("💡 Custom item - enter details manually")
                return
            
            # Look up item in database
            item = self.db.get_item(item_id)
            
            if item:
                # Auto-fill fields
                self.item_name_entry.delete(0, tk.END)
                self.item_name_entry.insert(0, item.name)
                
                self.item_desc_entry.delete(0, tk.END)
                self.item_desc_entry.insert(0, item.description)
                
                self.item_price_entry.delete(0, tk.END)
                self.item_price_entry.insert(0, str(item.price))
                
                # Disable fields (read-only)
                self.item_name_entry.config(state='readonly')
                self.item_desc_entry.config(state='readonly')
                self.item_price_entry.config(state='readonly')
                
                # Focus on quantity
                self.item_qty_entry.focus()
                
                self.display_message(f" Found: {item.name} - ${item.price:.2f}")
            else:
                self.clear_item_fields()
                self.enable_item_fields()
                self.display_message(f" Item ID {item_id} not found - enter manually or use ID 0")
                
        except ValueError:
            pass  # Ignore if not a valid number

    def clear_item_fields(self):
        """Clear all item entry fields"""
        self.item_name_entry.delete(0, tk.END)
        self.item_desc_entry.delete(0, tk.END)
        self.item_price_entry.delete(0, tk.END)

    def enable_item_fields(self):
        """Enable item fields for manual entry"""
        self.item_name_entry.config(state='normal')
        self.item_desc_entry.config(state='normal')
        self.item_price_entry.config(state='normal')

    def start_order(self):
        try:
            customer_name = self.customer_name_entry.get().strip()
            if not customer_name:
                messagebox.showwarning("Warning", "Please enter customer name")
                return
            
            # Check if there's already an active order
            if self.take_order.current_order is not None:
                response = messagebox.askyesno(
                    "Active Order", 
                    "There is already an active order. Do you want to cancel it and start a new one?"
                )
                if response:
                    self.take_order.cancel_order()
                    self.display_message("Previous order cancelled.\n")
                else:
                    return
            
            # Clear previous order messages
            self.display.config(state='normal')
            self.display.delete('1.0', tk.END)
            self.display.config(state='disabled')
            
            # Start the order
            self.take_order.start_new_order(self.next_order_id, customer_name)
            
            # Show the new order message
            self.display_message(f"✓ Started Order #{self.next_order_id} for {customer_name}")
            
            # Clear customer name field
            self.customer_name_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_item(self):
        try:
            item_id_str = self.item_id_entry.get().strip()
            if not item_id_str:
                messagebox.showerror("Error", "Please enter Item ID")
                return
                
            item_id = int(item_id_str)
            name = self.item_name_entry.get()
            desc = self.item_desc_entry.get()
            
            # Remove $ symbol if present
            price_str = self.item_price_entry.get().strip().replace('$', '')
            price = float(price_str)
            
            qty = int(self.item_qty_entry.get())

            item = Item(item_id, name, desc, price)
            
            # Save custom items (ID 0) to database with a unique ID
            if item_id == 0:
                # Generate a unique custom ID (use negative numbers for custom items)
                all_orders = self.db.get_all_orders(limit=1000)
                custom_id = -1 - len(all_orders)
                item = Item(custom_id, name, desc, price)
                self.db.add_item(item)
                self.display_message(f"Custom item '{name}' saved to database")
            else:
                # Save item to database if it doesn't exist
                existing = self.db.get_item(item_id)
                if not existing:
                    self.db.add_item(item)
                    self.display_message(f"Item '{name}' added to database")
            
            self.take_order.add_item_to_order(item, qty)
            self.display_message(f"Added {qty} x {name} (${price:.2f})")
            
            # Clear item fields
            self.item_id_entry.delete(0, tk.END)
            self.clear_item_fields()
            self.item_qty_entry.delete(0, tk.END)
            self.enable_item_fields()
            
            # Reset lookup tracking
            self._last_lookup_id = None
            
            # Focus back on item ID
            self.item_id_entry.focus()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
            if self.take_order.current_order is None:
                raise ValueError("No active order to checkout.")
            
            # Calculate total
            checkout_obj = OrderCheckout(self.take_order.current_order)
            total = checkout_obj.calculate_total()
            
            # Save order to database
            order_id = self.db.save_order(self.take_order.current_order, total)
            
            # Update order history
            self.take_order.order_history.append(self.take_order.current_order)
            self.take_order.current_order = None
            
            self.display_message(f"✓ Order #{self.next_order_id} checked out - Total: ${total:.2f}")
            self.display_message(f"✓ Saved to database as Order #{order_id}")
            
            # Increment order ID for next order
            self.next_order_id += 1
            self.update_order_id_display()
            
            # Clear customer name
            self.customer_name_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_order(self):
        try:
            self.take_order.cancel_order()
            self.display_message("Order cancelled.")
            
            # Clear customer name
            self.customer_name_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_message(self, msg: str):
        self.display.config(state='normal')  # Enable to write
        self.display.insert(tk.END, msg + "\n")
        self.display.see(tk.END)
        self.display.config(state='disabled')  # Disable again

    def on_closing(self):
        """Clean up database connection when closing"""
        if hasattr(self, 'db'):
            self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()