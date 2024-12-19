from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Database connection
def get_data():
    conn = psycopg2.connect(
        database="ecommerce",
        user="user",
        #password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_id, customer_firstname, customer_lastname, gender, birthdate, amount, purchase_date, merchant_name, category
        FROM transactions
        ORDER BY purchase_date DESC
        LIMIT 100
    """)
    data = cursor.fetchall()
    conn.close()
    return data

@app.route("/")
def index():
    transactions = get_data()
    return render_template("index.html", transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)
