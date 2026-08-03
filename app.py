import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    all_records = cursor.fetchall()
    conn.close()

    return render_template("index.html", expenses=all_records)

@app.route("/add", methods=["POST"])
def add():
    date = request.form['date']
    category = request.form['category']
    description = request.form['description']
    amount = request.form['amount']

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO expenses (date, category, description, amount)
    VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))

    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))

    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    if request.method == "POST":
        date = request.form['date']
        category = request.form['category']
        description = request.form['description']
        amount = request.form['amount']

        cursor.execute('''
        UPDATE expenses
        SET date = ?, category = ?, description = ?, amount = ?
        WHERE id = ? 
        ''', (date, category, description, amount, id))

        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    else:
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))

        expense = cursor.fetchone()
        conn.close()

        return render_template("edit.html", expense=expense)
        
if __name__ == "__main__":
    app.run(debug=True)