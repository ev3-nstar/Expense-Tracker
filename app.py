import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Run this once when the app starts to create the database file if it doesn't exist
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL
        )
    ''')

# The main home page
@app.route("/")
def home():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    # Grab all the expenses from the database so we can list them on the page
    cursor.execute("SELECT * FROM expenses")
    all_records = cursor.fetchall()
    conn.close()

    # Send the data over to the HTML file
    return render_template("index.html", expenses=all_records)

# This handles the "Add Expense" form when the user clicks submit
@app.route("/add", methods=["POST"])
def add():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    # Pull the exact text the user typed into the input boxes
    date = request.form['date']
    category = request.form['category']
    description = request.form['description']
    amount = request.form['amount']

    # Insert the new row
    cursor.execute('''
    INSERT INTO expenses (date, category, description, amount)
    VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))

    # Save the file changes
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# This runs when the user clicks the Delete button
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    # Removes the row where the ID matches the one passed in the URL
    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))

    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))

# This route does double-duty for the Edit page
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    # If the user clicked "Save Changes" on the edit form
    if request.method == "POST":
        date = request.form['date']
        category = request.form['category']
        description = request.form['description']
        amount = request.form['amount']

        # Overwrite the old row data with the new inputs
        cursor.execute('''
        UPDATE expenses
        SET date = ?, category = ?, description = ?, amount = ?
        WHERE id = ? 
        ''', (date, category, description, amount, id))

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    # If the user just clicked "Edit" and needs to see the pre-filled form
    else:

        # Fetch only the single row they want to edit
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))

        expense = cursor.fetchone()
        conn.close()

        return render_template("edit.html", expense=expense)
        
if __name__ == "__main__":
    app.run(debug=True)