import psycopg2
from tabulate import tabulate

# Database connection details
conn = psycopg2.connect(
    dbname="dvdrental",  # Database name
    user="postgres",  # Username
    password="password",  # Password
    host="localhost",
    port="5432"  # Default PostgreSQL port
)

cur = conn.cursor()

# Query to fetch the top 5 customers
query = """
SELECT 
    customer_id,
    COUNT(*) AS rental_count,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS rank
FROM rental
GROUP BY customer_id
ORDER BY rank
LIMIT 5;
"""
cur.execute(query)
rows = cur.fetchall()

# Define headers for the table
headers = ["Customer ID", "Rental Count", "Rank"]

# Display the results in a table format
with open ("test.txt", "w") as test:
    test.writelines((tabulate(rows, headers=headers, tablefmt="grid")))

# Close the cursor and connection
cur.close()
conn.close()
