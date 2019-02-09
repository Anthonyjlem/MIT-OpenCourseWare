annual_salary = float(input("Enter your annual salary: "))
monthly_salary = annual_salary/12
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))*monthly_salary
total_cost = float(input("Enter the cost of your dream home: "))
portion_down_payment = 0.25*total_cost
current_savings = 0
number_of_months = 0
r = 0.04

while portion_down_payment > current_savings:
    current_savings = current_savings + r*current_savings/12
    current_savings += portion_saved
    number_of_months += 1
print("Number of months:", number_of_months)
