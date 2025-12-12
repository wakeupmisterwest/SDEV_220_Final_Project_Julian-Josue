import sqlite3
from typing import List, Optional
from items import Item
from order import Order


class POSDatabase:
    """Handles all database operations for the POS system using SQLite."""

    def __init__(self, db_name: str = "pos_system.db"):
        """Initialize the database connection and create tables if they don't exist."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            # Enable foreign key support
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def create_tables(self):
        """Create all necessary tables for the POS system."""
        try:
            # Items/Menu table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    item_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    is_available INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Orders table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_amount REAL NOT NULL,
                    status TEXT DEFAULT 'completed'
                )
            """)

            # Order Items table (junction table)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    item_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    price_at_order REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                    FOREIGN KEY (item_id) REFERENCES items(item_id)
                )
            """)

            self.conn.commit()
            print("Database tables created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise

    # item operations

    def add_item(self, item: Item) -> bool:
        """Add a new item to the database."""
        try:
            self.cursor.execute("""
                INSERT INTO items (item_id, name, description, price)
                VALUES (?, ?, ?, ?)
            """, (item.itemID, item.name, item.description, item.price))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Item with ID {item.itemID} already exists.")
            return False
        except sqlite3.Error as e:
            print(f"Error adding item: {e}")
            return False

    def get_item(self, item_id: int) -> Optional[Item]:
        """Retrieve an item by its ID."""
        try:
            self.cursor.execute("""
                SELECT item_id, name, description, price
                FROM items
                WHERE item_id = ? AND is_available = 1
            """, (item_id,))
            
            row = self.cursor.fetchone()
            if row:
                return Item(row[0], row[1], row[2], row[3])
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving item: {e}")
            return None

    def get_all_items(self) -> List[Item]:
        """Retrieve all available items from the database."""
        try:
            self.cursor.execute("""
                SELECT item_id, name, description, price
                FROM items
                WHERE is_available = 1
                ORDER BY name
            """)
            
            items = []
            for row in self.cursor.fetchall():
                items.append(Item(row[0], row[1], row[2], row[3]))
            return items
        except sqlite3.Error as e:
            print(f"Error retrieving items: {e}")
            return []

    def update_item(self, item: Item) -> bool:
        """Update an existing item in the database."""
        try:
            self.cursor.execute("""
                UPDATE items
                SET name = ?, description = ?, price = ?
                WHERE item_id = ?
            """, (item.name, item.description, item.price, item.itemID))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating item: {e}")
            return False

    def delete_item(self, item_id: int) -> bool:
        """Soft delete an item (mark as unavailable)."""
        try:
            self.cursor.execute("""
                UPDATE items
                SET is_available = 0
                WHERE item_id = ?
            """, (item_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting item: {e}")
            return False

    # order operations

    def save_order(self, order: Order, total_amount: float) -> Optional[int]:
        """Save a completed order to the database."""
        try:
            # Insert the order
            self.cursor.execute("""
                INSERT INTO orders (customer_name, total_amount)
                VALUES (?, ?)
            """, (order.name, total_amount))
            
            order_id = self.cursor.lastrowid

            # Insert all order items
            for item, quantity in order.item_list:
                self.cursor.execute("""
                    INSERT INTO order_items (order_id, item_id, quantity, price_at_order)
                    VALUES (?, ?, ?, ?)
                """, (order_id, item.itemID, quantity, item.price))

            self.conn.commit()
            print(f"Order {order_id} saved successfully.")
            return order_id
        except sqlite3.Error as e:
            print(f"Error saving order: {e}")
            self.conn.rollback()
            return None

    def get_all_orders(self, limit: int = 100) -> List[dict]:
        """Retrieve recent orders with basic information."""
        try:
            self.cursor.execute("""
                SELECT order_id, customer_name, order_date, total_amount, status
                FROM orders
                ORDER BY order_date DESC
                LIMIT ?
            """, (limit,))
            
            orders = []
            for row in self.cursor.fetchall():
                orders.append({
                    'order_id': row[0],
                    'customer_name': row[1],
                    'order_date': row[2],
                    'total_amount': row[3],
                    'status': row[4]
                })
            return orders
        except sqlite3.Error as e:
            print(f"Error retrieving orders: {e}")
            return []

    # utility methods

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()