import mysql.connector
from mysql.connector import Error
import getpass

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=getpass.getpass("Enter MySQL root password: "),
            database="finance_tracker"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

# Register new user
def register_user(connection):
    cursor = connection.cursor()

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    monthly_income = float(input("Enter your monthly income: "))
    savings_goal = float(input("Enter your savings goal: "))

    query = "INSERT INTO user (name, email, password, monthly_income, savings_goal) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (name, email, password, monthly_income, savings_goal))
    connection.commit()

    print("✅ User registered successfully!")

# Add a transaction
def add_transaction(connection):
    cursor = connection.cursor()
    user_id = int(input("Enter your User ID: "))
    amount = float(input("Enter amount: "))
    trans_type = input("Enter type (income/expense): ").upper()  # match ENUM
    category = input("Enter category (e.g., food, rent, salary): ")
    trans_date = input("Enter date (YYYY-MM-DD): ")

    query = """INSERT INTO transactions (user_id, amount, type, category, txn_date)
               VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (user_id, amount, trans_type, category, trans_date))
    connection.commit()
    print("✅ Transaction added successfully!\n")

# View monthly summary
def view_summary(connection):
    cursor = connection.cursor()
    user_id = int(input("Enter your User ID: "))
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    query = """
        SELECT type, SUM(amount)
        FROM transactions
        WHERE user_id = %s AND MONTH(txn_date) = %s AND YEAR(txn_date) = %s
        GROUP BY type
    """
    cursor.execute(query, (user_id, month, year))
    results = cursor.fetchall()

    print("\n📊 Monthly Summary:")
    for row in results:
        print(f"{row[0]}: {row[1]}")
    print()

# Check savings goal using stored procedure
def check_savings_goal(connection):
    cursor = connection.cursor()
    user_id = int(input("Enter your User ID: "))
    month = int(input("Enter month (MM): "))
    year = int(input("Enter year (YYYY): "))

    cursor.callproc("CheckSavingsGoal", (user_id, month, year))
    for result in cursor.stored_results():
        message = result.fetchone()[0]
        print(f"\n💡 {message}\n")

# Main program loop
def main():
    connection = create_connection()
    if not connection:
        print("❌ Failed to connect to database.")
        return

    while True:
        print("==== Finance Tracker ====")
        print("1. Register User")
        print("2. Add Transaction")
        print("3. View Monthly Summary")
        print("4. Check Savings Goal")
        print("5. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            register_user(connection)
        elif choice == "2":
            add_transaction(connection)
        elif choice == "3":
            view_summary(connection)
        elif choice == "4":
            check_savings_goal(connection)
        elif choice == "5":
            print("👋 Exiting Finance Tracker. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice, try again.\n")

    connection.close()

if __name__ == "__main__":
    main()
