import sqlite3

# Create a new SQLite database and establish a connection
conn = sqlite3.connect('payroll.db')
cursor = conn.cursor()

# Create the 'employees' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        hourly_rate REAL
    )
''')

# Insert sample data into the 'employees' table
cursor.execute("INSERT INTO employees (employee_id, first_name, last_name, hourly_rate) VALUES ('1234', 'Wesly', 'Honore', 20.50)")
cursor.execute("INSERT INTO employees (employee_id, first_name, last_name, hourly_rate) VALUES ('5678', 'John', 'Doe', 18.75)")
cursor.execute("INSERT INTO employees (employee_id, first_name, last_name, hourly_rate) VALUES ('91011', 'Jane', 'Smith', 22.00)")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Employee table created and sample data inserted.")
