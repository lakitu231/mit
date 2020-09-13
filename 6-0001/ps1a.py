# House Hunting

portion_down_payment = 0.25
current_savings = 0
r = 0.04

annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

# Number of months is 0 if current_savings is enough for down payment
month = 0

# Increase in current_savings occurs in every end of months
while current_savings < portion_down_payment * total_cost:
    month += 1
    current_savings += r / 12 * current_savings + portion_saved * annual_salary / 12

print(f"Number of months: {month}")


















'''
In Part A, we are going to determine how long it will take you to save enough
money to make the down payment given the following assumptions:
1. Call the cost of your dream home ​total_cost​.
2. Call the portion of the cost needed for a down payment ​portion_down_payment​. For
simplicity, assume that portion_down_payment = 0.25 (25%).
3. Call the amount that you have saved thus far ​current_savings​. You start with a current
savings of $0.
4. Assume that you invest your current savings wisely, with an annual return of ​r ​(in other words,
at the end of each month, you receive an additional ​current_savings*r/12​ funds to put into
your savings – the 12 is because ​r​ is an annual rate). Assume that your investments earn a
return of r = 0.04 (4%).
5. Assume your annual salary is ​annual_salary​.
6. Assume you are going to dedicate a certain amount of your salary each month to saving for
the down payment. Call that ​portion_saved​. This variable should be in decimal form (i.e. 0.1
for 10%).
7. At the end of each month, your savings will be increased by the return on your investment,
plus a percentage of your ​monthly salary ​(annual salary / 12).
    
Your program should ask the user to enter the following variables:
1. The starting annual salary (annual_salary)
2. The portion of salary to be saved (portion_saved)
3. The cost of your dream home (total_cost)

Test Case 1
>>>
Enter your annual salary:​ 120000
Enter the percent of your salary to save, as a decimal: . ​ 10
Enter the cost of your dream home:​ 1000000
Number of months:​ 183
>>>
Test Case 2
>>>
Enter your annual salary:​ 80000
Enter the percent of your salary to save, as a decimal: . ​ 15
Enter the cost of your dream home:​ 500000
Number of months:​ 105
>>>
'''