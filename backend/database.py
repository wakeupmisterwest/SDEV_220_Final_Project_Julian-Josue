import sqlite3
from typing import List, Optional
from items import Item
from order import Order
import csv
import os
from datetime import date


class POSDatabase:
   #handles all database operations for the POS system using sqlite

    def __init__(self, db_name: str = "pos_system.db"):
        #this initialize the database connection and create tables if they dont exist
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def close(self):
        #Close the database connection cleanly
        try:
            if getattr(self, "cursor", None):
                self.cursor.close()
            if getattr(self, "conn", None):
                self.conn.close()
        except Exception:
            pass

    def connect(self):
        #establish connection to the SQLite database
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            # Enables foreign key support
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def create_tables(self):
        #Creates the tables for the POS system
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
       #adds a new item to the database
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

    def get_item(self, item_id: int) -> Optional[Item]:    # it can either return an item obj or none
        #Retrieves an item by its ID
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
        #retrieves all available items from the database
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
        #Updates an existing item in the database
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
        #Deletes an item when removed with remove item
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
        #Saves a completed order to the database
        try:
            #Inserts the order
            self.cursor.execute("""
                INSERT INTO orders (customer_name, total_amount)
                VALUES (?, ?)
            """, (order.name, total_amount))
            
            order_id = self.cursor.lastrowid

            #Inserts all order items
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
        #Retrieves recent orders
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
# export to .csv
    def export_end_of_day_csv(self, report_date: str | None = None, out_dir: str = "reports") -> str | None:
        if report_date is None:
            report_date = date.today().isoformat()

        os.makedirs(out_dir, exist_ok=True)
        filepath = os.path.join(out_dir, f"end_of_day_{report_date}.csv")

        try:
            self.cursor.execute("""
                SELECT
                    o.order_id,
                    date(o.order_date) as order_date,
                    o.customer_name,
                    i.item_id,
                    i.name as item_name,
                    oi.quantity,
                    oi.price_at_order,
                    (oi.quantity * oi.price_at_order) as line_total,
                    o.total_amount as order_total
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                JOIN items i ON oi.item_id = i.item_id
                WHERE date(o.order_date) = date(?)
                AND o.status = 'completed'
                ORDER BY o.order_id ASC
            """, (report_date,))

            cols = [d[0] for d in self.cursor.description]
            rows = self.cursor.fetchall()

            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(cols)   # header
                writer.writerows(rows)  # data

            return filepath
        except Exception as e:
            print(f"Error exporting end-of-day report: {e}")
            return None
