"""
End of Day Report Generator
Run this at the end of each day to generate a sales report
"""

import sys
import os
from datetime import datetime, date

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import POSDatabase

def generate_end_of_day_report():
    # Get today's date
    today = date.today().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create filename with today's date
    filename = f"EOD_Report_{today}.txt"
    
    print(f"\n📊 Generating End of Day Report for {today}...")
    
    db = POSDatabase("restaurant.db")
    
    # Get all orders (we'll filter by today)
    all_orders = db.get_all_orders(limit=1000)
    
    # Filter orders from today
    today_orders = []
    for order in all_orders:
        order_date = order['order_date'].split()[0]  # Get date part only
        if order_date == today:
            today_orders.append(order)
    
    # Calculate totals
    total_orders = len(today_orders)
    total_revenue = sum(order['total_amount'] for order in today_orders)
    
    # Count items sold today
    items_sold = {}
    for order in today_orders:
        # Note: We'd need to query order_items table to get item breakdown
        # For now, we'll just show order totals
        pass
    
    # Write report to file
    with open(filename, 'w') as f:
        # Header
        f.write("="*70 + "\n")
        f.write(" 📊 END OF DAY REPORT\n")
        f.write("="*70 + "\n")
        f.write(f" Date: {today}\n")
        f.write(f" Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        # Summary
        f.write("💰 SALES SUMMARY\n")
        f.write("-"*70 + "\n")
        f.write(f"  Total Orders Today:    {total_orders}\n")
        f.write(f"  Total Revenue:         ${total_revenue:.2f}\n")
        if total_orders > 0:
            f.write(f"  Average Order Value:   ${total_revenue/total_orders:.2f}\n")
        f.write("\n")
        
        # Individual Orders
        f.write("📦 TODAY'S ORDERS\n")
        f.write("-"*70 + "\n")
        
        if today_orders:
            for i, order in enumerate(today_orders, 1):
                f.write(f"\n  {i}. Order #{order['order_id']}\n")
                f.write(f"     Customer:  {order['customer_name']}\n")
                f.write(f"     Time:      {order['order_date'].split()[1]}\n")
                f.write(f"     Total:     ${order['total_amount']:.2f}\n")
        else:
            f.write("\n  ❌ No orders today\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write(" End of Report\n")
        f.write("="*70 + "\n")
    
    db.close()
    
    # Print summary to console
    print(f"\n✅ Report saved to: {filename}")
    print(f"\n📊 Summary for {today}:")
    print(f"   - Total Orders: {total_orders}")
    print(f"   - Total Revenue: ${total_revenue:.2f}")
    if total_orders > 0:
        print(f"   - Average Order: ${total_revenue/total_orders:.2f}")
    print()

if __name__ == "__main__":
    try:
        generate_end_of_day_report()
    except FileNotFoundError:
        print("\n❌ Error: restaurant.db not found!")
        print("   Make sure the database file exists.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")