import sys
from db_connection import get_cursor, close_connection
from formatting import print_table

def login_menu(conn):
    """
    Display the login menu and handle user authentication for admins.
    """
    cur = get_cursor(conn)
    print("\n" + "="*30)
    print("        LOGIN MENU        ")
    print("="*30)
    print("1. Login as Admin")
    print("2. Login as Customer")
    print("0. Exit")
    print("="*30)
    
    lg_choice = input("\nEnter your choice: ").strip()
    
    if lg_choice == "0":
        print("\nThank you for using our service!")
        close_connection(cur, conn)
        sys.exit()
    elif lg_choice == "1":
        print("\n" + "="*30)
        print("       ADMIN LOGIN        ")
        print("="*30)
        uname = input("Enter admin username: ").strip()
        pwd = input("Enter admin password: ").strip()
        
        try:
            cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (uname, pwd))
            data = cur.fetchone()
            
            if data is None:
                print("\nInvalid username or password! Please try again.")
                login_menu(conn)
            else:
                print("\nLogin successful! Redirecting to Admin Menu...")
                admin_menu(conn)
                
        except Exception as e:
            print(f"\nError during login: {e}")
        finally:
            close_connection(cur, conn)
    elif lg_choice == "2":
        customer_menu(conn)
    else:
        print("\nInvalid choice! Please select a valid option.")
        login_menu(conn)

def customer_menu(conn):
    """
    Display the customer menu and handle various customer operations.
    """
    print("\n" + "="*30)
    print("       CUSTOMER MENU      ")
    print("="*30)
    print("1. View Items")
    print("2. Place Order")
    print("0. Exit")
    print("="*30)
    
    cs_choice = input("\nEnter your choice: ").strip()
    
    if cs_choice == "1":
        view_items(conn, lg_choice="2")
    elif cs_choice == "2":
        payment(conn, lg_choice="2")
    elif cs_choice == "0":
        print("\nLogging out... Thank you for visiting!")
        login_menu(conn)
    else:
        print("\nInvalid choice! Please try again.")
        customer_menu(conn)

def admin_menu(conn):
    """
    Display the admin menu and handle various admin operations.
    """
    print("\n" + "="*30)
    print("        ADMIN MENU        ")
    print("="*30)
    print("1. Add Item")
    print("2. Remove Item")
    print("3. View Items")
    print("4. View Orders")
    print("5. Process Payment")
    print("6. Delete Order")
    print("0. Logout")
    print("="*30)
    
    ad_choice = input("\nEnter your choice: ").strip()
    
    if ad_choice == "1":
        add_item(conn)
    elif ad_choice == "2":
        remove_item(conn)
    elif ad_choice == "3":
        view_items(conn, lg_choice="1")
    elif ad_choice == "4":
        view_orders(conn)
    elif ad_choice == "5":
        payment(conn, lg_choice="1")
    elif ad_choice == "6":
        delete_order(conn)
    elif ad_choice == "0":
        print("\nLogging out... See you soon!")
        login_menu(conn)
    else:
        print("\nInvalid choice! Please try again.")
        admin_menu(conn)

def add_item(conn):
    """
    Add a new food item to the food_items table.
    """
    print("\n" + "="*30)
    print("         ADD ITEM         ")
    print("="*30)
    name = input("Enter item name: ").strip()
    price = input("Enter item price: ").strip()
    
    cur = get_cursor(conn)
    cur.execute(
        "INSERT INTO food_items (name, price) VALUES (%s, %s)",
        (name, price)
    )
    conn.commit()
    print(f"\nItem '{name}' added successfully!")
    admin_menu(conn)

def view_items(conn, lg_choice=None):
    """
    Display all food items from the food_items table in a formatted table.
    """
    print("\n" + "="*30)
    print("        VIEW ITEMS        ")
    print("="*30)
    cur = get_cursor(conn)
    cur.execute("SELECT item_id, name, price FROM food_items")
    data = cur.fetchall()
    
    if not data:
        print("No items found.")
    else:
        headers = ["ID", "Name", "Price"]
        rows = [[str(item[0]), item[1], f"${item[2]:.2f}"] for item in data]
        print_table(headers, rows)
            
    if lg_choice == "1":
        admin_menu(conn)
    elif lg_choice == "2":
        customer_menu(conn)
    else:
        login_menu(conn)

def view_orders(conn):
    """
    Display all payment records from the payments table in a formatted table.
    """
    print("\n" + "="*30)
    print("       VIEW PAYMENTS      ")
    print("="*30)
    
    cur = get_cursor(conn)
    cur.execute("""
        SELECT payment_id, customer_name, item_id, quantity, item_price, payment_date, payment_method
        FROM payments
    """)
    data = cur.fetchall()
    
    if not data:
        print("No payments found!")
    else:
        headers = ["ID", "Customer", "Item ID", "Qty", "Total Price", "Date", "Method"]
        rows = [
            [
                str(row[0]), 
                row[1], 
                str(row[2]), 
                str(row[3]), 
                f"${row[4]:.2f}", 
                row[5].strftime('%Y-%m-%d %H:%M:%S'), 
                row[6]
            ] 
            for row in data
        ]
        print_table(headers, rows)
        
    admin_menu(conn)

def remove_item(conn):
    """
    Remove a food item from the food_items table using the item ID.
    """
    print("\n" + "="*30)
    print("       REMOVE ITEM        ")
    print("="*30)
    item_id = input("Enter item ID to remove: ").strip()
    
    cur = get_cursor(conn)
    cur.execute("SELECT * FROM food_items WHERE item_id = %s", (item_id,))
    if cur.fetchone():
        cur.execute("DELETE FROM food_items WHERE item_id = %s", (item_id,))
        conn.commit()
        print(f"\nItem ID '{item_id}' removed successfully!")
    else:
        print("\nInvalid item ID!")
    admin_menu(conn)

def payment(conn, lg_choice):
    """
    Process payment for an order.
    """
    cur = get_cursor(conn)
    try:
        print("\n" + "="*30)
        print("         PAYMENT          ")
        print("="*30)
        try:
            item_id = int(input("Enter item ID: "))
        except ValueError:
            print("\nPlease enter a valid item ID.")
            payment(conn, lg_choice)
            return

        cur.execute("SELECT * FROM food_items WHERE item_id = %s", (item_id,))
        item = cur.fetchone()
        if item is None:
            print("\nItem not found!")
            customer_menu(conn)
            return

        item_name = item[1]
        item_price = item[2]

        print(f"\nSelected Item: {item_name} - ${item_price:.2f}")
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("\nPlease enter a valid quantity.")
            payment(conn, lg_choice)
            return

        total_price = item_price * quantity
        print(f"\nTotal Price: ${total_price:.2f}")
        payment_method = input("Enter payment method (Cash, Card, Online): ").strip() or "Cash"
        customer_name = input("Enter your name: ").strip()

        cur.execute(
            """
            INSERT INTO payments (customer_name, item_id, quantity, item_price, payment_date, payment_method)
            VALUES (%s, %s, %s, %s, now(), %s)
            """,
            (customer_name, item_id, quantity, total_price, payment_method)
        )
        conn.commit()
        print("\nPayment recorded successfully!")
        print("="*30)
        if lg_choice == "1":
            admin_menu(conn)
        elif lg_choice == "2":
            customer_menu(conn)
        else:
            login_menu(conn)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        cur.close()

def delete_order(conn):
    """
    Delete an order from the payments table using the payment ID.
    """
    print("\n" + "="*30)
    print("       DELETE ORDER       ")
    print("="*30)
    payment_id = input("Enter payment ID to delete: ").strip()
    
    cur = get_cursor(conn)
    cur.execute("SELECT * FROM payments WHERE payment_id = %s", (payment_id,))
    if cur.fetchone():
        cur.execute("DELETE FROM payments WHERE payment_id = %s", (payment_id,))
        conn.commit()
        print(f"\nOrder ID '{payment_id}' deleted successfully!")
    else:
        print("\nInvalid payment ID!")
    admin_menu(conn)
