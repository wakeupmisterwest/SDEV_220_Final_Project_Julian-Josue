from database import POSDatabase
from items import Item

db = POSDatabase("restaurant.db")

# Add your menu
menu = [
    Item(1, "Cheeseburger", "Classic cheeseburger", 9.99),
    Item(2, "Beef Burger", "Plain beef burger", 8.99),
    Item(3, "Fries", "French fries", 3.99),
    Item(4, "Coke", "Coca Cola", 2.49),
    Item(5, "Water", "Bottled water", 1.99),
]

for item in menu:
    db.add_item(item)
    print(f"Added: {item.name}")

db.close()
print("\n✓ Menu items added!")