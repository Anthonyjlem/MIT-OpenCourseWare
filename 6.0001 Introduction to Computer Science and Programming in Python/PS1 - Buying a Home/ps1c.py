annual_salary = float(input("Enter the starting salary: "))
monthly_salary = annual_salary/12
total_cost = 12888000
portion_down_payment = 0.25*total_cost
current_savings = 0
number_of_months = 0
r = 0.04
semi_annual_raise = 0.07
epsilon = 100
steps = 0
low = 0
high = 10000
avg = (low+high)/2
months = 0

while abs(portion_down_payment - current_savings) >= epsilon:
    steps += 1
    current_savings = 0
    while months < 36:
        current_savings = current_savings + r*current_savings/12
        current_savings += avg/10000*monthly_salary
        if months % 6 == 0:
            monthly_salary += semi_annual_raise*monthly_salary
        months += 1
    if current_savings > portion_down_payment:
        high = avg
    else:
        low = avg
    avg = (low+high)/2
    monthly_salary = annual_salary/12
    months = 0
    if 1-avg/10000 < 0.0001:
        break

if abs(portion_down_payment - current_savings) < epsilon:
    print("Best savings rate:", avg/10000, '\n' + "Steps in bisection search:", steps)
else:
    print("It is not possible to pay the down payment in three years.")
