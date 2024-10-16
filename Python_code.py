import pandas as pd
import csv
import os


# Constants
passwords = ["PW121", "PW122", "PW123", "PW133", "PW211", "PW212", "PW213", "PW221", "PW223", "PW231"]
default_hourly_rate = 20.0

# Initialize variables
hourly_rate = default_hourly_rate

# MODULE 1: Security Check
def get_password():
    print("Please enter your password:")
    password = input()  # Simple input, no masking here in Python
    return password

def check_password(password):
    if password in passwords:
        print("Password verified.")
        return True
    print("Incorrect password.")
    return False

# MODULE 2: Employee Information
def get_employee_info():
    global hourly_rate

    password = get_password()
    if not check_password(password):
        print("Invalid password!")
        return None

    first_name = input("Enter employee first name: ")
    last_name = input("Enter employee last name: ")
    employee_id = int(input("Enter employee ID: "))
    num_dependents = int(input("Number of dependents: "))
    hours_worked = float(input("Hours worked: "))

    # Retrieve hourly rate from the database or input
    try:
        hourly_pay = float(input(f"Enter hourly rate for employee ID {employee_id} (or press Enter to use default ${hourly_rate}): "))
        if hourly_pay > 0:
            hourly_rate = hourly_pay
    except ValueError:
        print("Invalid hourly rate. Using default rate.")

    return {
        "first_name": first_name,
        "last_name": last_name,
        "employee_id": employee_id,
        "num_dependents": num_dependents,
        "hours_worked": hours_worked,
        "hourly_pay": hourly_rate
    }

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

# MODULE 4: Tax Calculation
def calculate_taxes(gross_income, num_dependents):
    dep_total = num_dependents * 25 if num_dependents > 0 else 0
    state_tax = gross_income * 0.056
    fed_tax = gross_income * 0.079
    net_income = gross_income - (state_tax + fed_tax + dep_total)
    return state_tax, fed_tax, dep_total, net_income

# MODULE 5: Writing Report and Sending to Printer
def write_employee_report_and_send_to_printer(employee_info, gross_income, state_tax, fed_tax, dep_total, net_income):
    print("Logging employee report to a text file and sending it to the printer...")

    # Create the employee report
    report = (
        f"Employee Report\n"
        f"================\n"
        f"First Name: {employee_info['first_name']}\n"
        f"Last Name: {employee_info['last_name']}\n"
        f"Employee ID: {employee_info['employee_id']}\n"
        f"Number of Dependents: {employee_info['num_dependents']}\n"
        f"Hours Worked: {employee_info['hours_worked']}\n"
        f"Hourly Rate: ${employee_info['hourly_pay']}\n"
        f"Gross Income: ${gross_income}\n"
        f"State Tax: ${state_tax}\n"
        f"Federal Tax: ${fed_tax}\n"
        f"Dependent Deduction: ${dep_total}\n"
        f"Net Income: ${net_income}\n"
        f"================\n"
    )

    # Print the report before sending to the printer
    print(report)

    # Append the report to a log file
    with open("employee_reports.txt", "a") as file_handle:
        file_handle.write(report)

    # Simulate sending the report to the printer (just prints to the console here)
    print("Sending report to the printer...")

# MODULE 6: Writing to CSV File
def write_employee_data_to_csv(employee_info):
    print("Writing employee data to the CSV file...")

    # Write the employee information to the CSV file
    with open("employees.csv", mode="a", newline="") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow([employee_info["first_name"], employee_info["last_name"], employee_info["employee_id"],
                         employee_info["num_dependents"], employee_info["hours_worked"], employee_info["hourly_pay"]])

    print("Employee data has been written to employees.csv")

# MODULE 7: Opening the CSV in Excel
def open_csv_in_excel():
    print("Opening employees.csv in Excel...")
    os.system("start excel employees.csv")

# MODULE 8: User Loop for Input and Printing
def process_employee_requests():
    while True:
        employee_info = get_employee_info()

        if employee_info is None:
            continue

        gross_income = calculate_gross_income(employee_info['hourly_pay'], employee_info['hours_worked'])
        state_tax, fed_tax, dep_total, net_income = calculate_taxes(gross_income, employee_info['num_dependents'])

        # Print and log employee report, then send it to the printer
        write_employee_report_and_send_to_printer(employee_info, gross_income, state_tax, fed_tax, dep_total, net_income)

        # Write employee data to CSV for database purposes
        write_employee_data_to_csv(employee_info)

        # Ask the user if they want to add another employee
        add_more = input("Do you want to add another employee? (yes/no): ")

        if add_more.lower() == "no":
            break

# Load hourly rates from the Excel file if needed (example)
def load_hourly_rates_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        # Assuming the Excel file has 'employeeID' and 'hourlyRate' columns
        for index, row in df.iterrows():
            # Here you might want to populate a dictionary for employeeID and their hourly rate
            print(f"ID: {row['employeeID']}, Hourly Rate: {row['hourlyRate']}")
    except Exception as e:
        print(f"Error reading Excel file: {e}")

# Uncomment the next line to load hourly rates when the program starts
# load_hourly_rates_from_excel("path_to_your_excel_file.xlsx")

# Start processing employee requests
process_employee_requests()
