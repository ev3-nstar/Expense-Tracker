import sqlite3
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL

        )
""")   

conn.commit()

def add_expense(date, category, description, amount):
    sql_command = """
        INSERT INTO expenses (date, category, description, amount)
        VALUES(?, ?, ?, ?)
    """
    data_tuple = (date, category, description, amount)

    cursor.execute(sql_command, data_tuple)
    conn.commit()
    print("Expense added succesfully!")

def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    all_records = cursor.fetchall()

    print("\n--- Your Expenses ---")
    for record in all_records:
        print(f"ID: {record[0]} | Date: {record[1]} | {record[2]}: {record[3]}| Cost: ${record[4]:.2f}")
        print("---------------------\n")

def delete_expense(expense_id):
    sql_command = "DELETE FROM expenses WHERE id = ?"
    cursor.execute(sql_command, (expense_id,))
    conn.commit()

    print(f"Expense ID {expense_id} has been deleted.")
def update_expense(expense_id, new_date, new_category, new_description, new_amount):
    sql_command = """
        UPDATE expenses
        SET date = ?, category = ?, description = ?, amount = ?
        WHERE id = ?
    """
    data_tuple = (new_date, new_category, new_description, new_amount, expense_id)

    cursor.execute(sql_command, data_tuple)
    conn.commit()

    print(f"Expense ID {expense_id} has been succesfully updated.")

while True:
    print("\n --- Expenses Tracker Menu ---")
    print ("1. Add a new expense")
    print("2. View all expenses")
    print("3. Update an expense")
    print("4. Delete an expense")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")
    if choice == '1':
        print("\n --- Add New Expense---")
        date = input("Enter the date (YYYY-MM-DD):")
        category = input("Enter the category: ")
        description = input("Enter a description: ")
        amount = float(input("Enter the amount: "))
        add_expense(date, category, description, amount)

    elif choice =='2':
        view_expenses()

    elif choice == '3':
        print("\n --- Update Expense ---")
        expense_id = int(input("Enter the ID of the expense to update: "))

        new_date = input("Enter the new date (YYYY-MM-DD): ")
        new_category = input("Enter the new category: ")
        new_description = input("Enter a new description: ")
        new_amount = float(input("Enter the new amount: "))

        update_expense(expense_id,new_date, new_category, new_category, new_description, new_amount)

    elif choice == '4':
        print("\n --- Delete Expense ---")
        expense_id = int(input("Enter the ID of the expense to delete: "))
        delete_expense(expense_id)

    elif choice == '5':
        print("Exiting proggram.")
        conn.close()
        break 
    else:
        print("Please enter a number between 1-5.")