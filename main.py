import sys
import display
from db_connection import get_database_connection, close_connection
from set_tables import set_tables

def main():
    """
    Main function to start the canteen automation system.
    """
    print("=" * 60)
    print("\n\tWELCOME TO CANTEEN AUTOMATION SYSTEM\n")
    print("=" * 60)
    
    # Establish a database connection
    conn = get_database_connection()
    if conn is None:
        print("\nFailed to connect to the database. Exiting...")
        sys.exit(1)

    try:
        # Start the login menu
        display.login_menu(conn)
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        close_connection(None, conn)
        print("Database connection closed.")

if __name__ == "__main__":
    # Set up database tables if they don't exist
    set_tables()
    # Run the main function
    main()
