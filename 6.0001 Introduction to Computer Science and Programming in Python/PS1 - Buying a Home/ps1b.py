annual_salary = float(input("Enter your annual salary: "))
monthly_salary = annual_salary/12
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
portion_down_payment = 0.25*total_cost
current_savings = 0
number_of_months = 0
r = 0.04
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

while portion_down_payment > current_savings:
    current_savings = current_savings + r*current_savings/12
    current_savings += portion_saved*monthly_salary
    number_of_months += 1
    if number_of_months % 6 == 0 and number_of_months > 0:
        monthly_salary += semi_annual_raise*monthly_salary
print("Number of months:", number_of_months)
