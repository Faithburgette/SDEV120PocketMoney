import os
import csv
import getpass
import sqlite3

# Create a SQLite database and employee table if it doesn't exist
def setup_database():
    conn = sqlite3.connect('employee_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employeeID INTEGER PRIMARY KEY,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            numDependents INTEGER,
            hoursWorked REAL,
            hourlyPay REAL
        )
    ''')
    conn.commit()
    conn.close()

import getpass

# MODULE 1: Security Check
def get_password():
    print("Please enter your password:")
    password = getpass.getpass(prompt='Password: ')  # Masked input
    return password

def get_passwords_from_file():
    with open('passwords.txt', 'r') as f:
        return [line.strip() for line in f]

def check_password(password):
    accepted_passwords = get_passwords_from_file()
    
    if password in accepted_passwords:
        return True
    else:
        print("Access denied")
        return False

# MODULE 2: Employee Information
def get_employee_info():
    password = get_password()  # password entered is masked

    if not check_password(password):
        print("Invalid password!")
        return None

    first_name = input("Enter employee first name: ")
    last_name = input("Enter employee last name: ")
    employee_id = int(input("Enter employee ID: "))
    num_dependents = int(input("Number of dependents: "))
    hours_worked = float(input("Hours worked: "))
    hourly_pay = get_hourly_rate_from_db()

    return {
        "firstName": first_name,
        "lastName": last_name,
        "employeeID": employee_id,
        "numDependents": num_dependents,
        "hoursWorked": hours_worked,
        "hourlyPay": hourly_pay
    }

def get_hourly_rate_from_db():
    # Simulate getting hourly rate from a database
    return 20.0  # example hourly rate

# MODULE 3: Payroll Calculation
def calculate_gross_income(hourly_pay, hours_worked):
    if hours_worked > 40:
        base_pay = hourly_pay * 40
        overtime_pay = (hours_worked - 40) * hourly_pay * 1.5
    else:
        base_pay = hourly_pay * hours_worked
        overtime_pay = 0
    gross_income = base_pay + overtime_pay
    return gross_income

def calculate_taxes(gross_income):
    state_tax = gross_income * 0.05
    fed_tax = gross_income * 0.10
    net_income = gross_income - state_tax - fed_tax
    return state_tax, fed_tax, net_income

# MODULE 4: Writing Report and Sending to Printer
def write_employee_report_and_send_to_printer(employee_info, gross_income, state_tax, fed_tax, net_income):
    print("Logging employee report to a text file and sending it to the printer...")

    # Create the employee report
    report = (
        "Employee Report\n"
        "================\n"
        f"First Name: {employee_info['firstName']}\n"
        f"Last Name: {employee_info['lastName']}\n"
        f"Employee ID: {employee_info['employeeID']}\n"
        f"Number of Dependents: {employee_info['numDependents']}\n"
        f"Hours Worked: {employee_info['hoursWorked']}\n"
        f"Hourly Rate: ${employee_info['hourlyPay']}\n"
        f"Gross Income: ${gross_income}\n"
        f"State Tax: ${state_tax}\n"
        f"Federal Tax: ${fed_tax}\n"
        f"Net Income: ${net_income}\n"
        "================\n"
    )

    # Print the report before sending to the printer
    print(report)

    # Append the report to a log file
    with open("employee_reports.txt", "a") as file_handle:
        file_handle.write(report)

    # Send the report to the default printer
    with open("temp_report.txt", "w") as temp_file:
        temp_file.write(report)

    # Send to printer (adjust for your OS)
    if os.name == 'nt':
        os.system("print temp_report.txt")  # Windows
    else:
        os.system("lp temp_report.txt")  # Unix-based systems (Linux/macOS)

    print("Report has been logged and sent to the printer.")

# MODULE 6: Writing to CSV File
def write_employee_data_to_csv(employee_info):
    print("Writing employee data to the CSV file...")

    # Open the CSV file in append mode
    with open("employees.csv", mode="a", newline="") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow([
            employee_info['firstName'],
            employee_info['lastName'],
            employee_info['employeeID'],
            employee_info['numDependents'],
            employee_info['hoursWorked'],
            employee_info['hourlyPay']
        ])

    print("Employee data has been written to employees.csv")

# MODULE 7: Writing to SQLite Database
def write_employee_to_db(employee_info):
    conn = sqlite3.connect('employee_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO employees (employeeID, firstName, lastName, numDependents, hoursWorked, hourlyPay)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        employee_info['employeeID'],
        employee_info['firstName'],
        employee_info['lastName'],
        employee_info['numDependents'],
        employee_info['hoursWorked'],
        employee_info['hourlyPay']
    ))

    conn.commit()
    conn.close()
    print("Employee data has been written to the database.")

# MODULE 8: Opening the CSV in Excel
def open_csv_in_excel():
    print("Opening employees.csv in Excel...")
    if os.name == 'nt':
        os.system("start excel employees.csv")  # Windows
    else:
        print("Opening in Excel is only supported on Windows.")

# MODULE 5: User Loop for Input and Printing
def process_employee_requests():
    setup_database()  # Ensure the database is set up before processing requests

    while True:
        employee_info = get_employee_info()

        if employee_info is None:
            continue

        gross_income = calculate_gross_income(employee_info['hourlyPay'], employee_info['hoursWorked'])
        state_tax, fed_tax, net_income = calculate_taxes(gross_income)

        write_employee_report_and_send_to_printer(employee_info, gross_income, state_tax, fed_tax, net_income)
        write_employee_data_to_csv(employee_info)
        write_employee_to_db(employee_info)  # Write to SQLite database

        add_more = input("Do you want to add another employee? (yes/no): ")
        if add_more.lower() == "no":
            break

if __name__ == "__main__":
    process_employee_requests()
