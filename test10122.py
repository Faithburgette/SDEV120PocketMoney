import sqlite3

def get_employee_data():
    first_name = input("Enter employee's first name: ")
    last_name = input("Enter employee's last name: ")
    employee_id = input("Enter employee ID: ")
    num_dependents = int(input("Enter number of dependents: "))
    hours_worked = float(input("Enter hours worked: "))
    
    # Database retrieval simulation
    hourly_rate = get_hourly_rate_from_db(employee_id)
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'employee_id': employee_id,
        'num_dependents': num_dependents,
        'hours_worked': hours_worked,
        'hourly_rate': hourly_rate
    }

def get_hourly_rate_from_db(employee_id):
    # Mock database query for hourly rate based on employee ID
    conn = sqlite3.connect('payroll.db')
    cursor = conn.cursor()
    cursor.execute("SELECT hourly_rate FROM employees WHERE employee_id = ?", (employee_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return 0.0  # Return default rate if employee not found
def calculate_payroll(employee):
    hourly_rate = employee['hourly_rate']
    hours_worked = employee['hours_worked']
    
    # Overtime calculation
    if hours_worked > 40:
        base_pay = hourly_rate * 40
        overtime_pay = (hours_worked - 40) * (hourly_rate * 1.5)
    else:
        base_pay = hourly_rate * hours_worked
        overtime_pay = 0
    
    gross_income = base_pay + overtime_pay
    
    # Dependents deduction ($25 per dependent)
    dep_total = employee['num_dependents'] * 25
    
    # Pre-tax amount calculation
    pre_tax_amount = gross_income
    
    # State and federal taxes
    state_tax = pre_tax_amount * 0.056
    fed_tax = pre_tax_amount * 0.079
    
    # Post-tax amount calculation
    post_tax_amount = pre_tax_amount - (state_tax + fed_tax)
    
    # Final amount after dependents deduction
    final_amount = post_tax_amount - dep_total
    
    return {
        'gross_income': gross_income,
        'state_tax': state_tax,
        'fed_tax': fed_tax,
        'post_tax_amount': post_tax_amount,
        'final_amount': final_amount
    }
def print_payroll_report(employee, payroll):
    print("\nEmployee Payroll Report")
    print("========================")
    print(f"First Name: {employee['first_name']}")
    print(f"Last Name: {employee['last_name']}")
    print(f"Employee ID: {employee['employee_id']}")
    print(f"Number of Dependents: {employee['num_dependents']}")
    print(f"Hours Worked: {employee['hours_worked']}")
    print(f"Hourly Rate: ${employee['hourly_rate']:.2f}")
    print(f"Gross Income: ${payroll['gross_income']:.2f}")
    print(f"State Tax: ${payroll['state_tax']:.2f}")
    print(f"Federal Tax: ${payroll['fed_tax']:.2f}")
    print(f"Post-Tax Amount: ${payroll['post_tax_amount']:.2f}")
    print(f"Final Amount After Deductions: ${payroll['final_amount']:.2f}")
    print("========================\n")
employee = get_employee_data()
payroll = calculate_payroll(employee)
print_payroll_report(employee, payroll)
