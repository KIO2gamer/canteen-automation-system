from db_connection import get_database_connection, get_cursor

def set_tables():
    """Set up the tables in the database."""
    # Create the tables
    conn = get_database_connection()
    cursor = get_cursor(conn)
    if cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS admin (
                admin_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS food_items (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name INT NOT NULL,
                item_id INT NOT NULL,
                quantity INT NOT NULL,
                item_price DECIMAL(10, 2) NOT NULL,
                payment_date DATE NOT NULL,
                payment_method ENUM('Cash', 'Card', 'Online'),
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
            """
        )
        conn.commit()
    else:
        print("Failed to create tables.")
    conn.close()