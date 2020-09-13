# Saving, with a raise



portion_down_payment = 0.25
current_savings = 0
r = 0.04

annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semiannual raise, as a decimal: "))

# Number of months is 0 if current_savings is enough for down payment
month = 0

# Increase in current_savings occurs in every end of months
while current_savings < portion_down_payment * total_cost:
    
    month += 1
    if month % 6 == 0:
        annual_salary += semi_annual_raise * annual_salary
    
    current_savings += r / 12 * current_savings + portion_saved * annual_salary / 12

print(f"Number of months: {month}")











'''
Modify your program to include the following
1. Have the user input a semi-annual salary raise ​semi_annual_raise​ (as a decimal percentage)
2. After the 6​th​ month, increase your salary by that percentage. Do the same after the 12th month, the 18​ ​ month, and so on

Have the user enter the following variables:
1. The starting annual salary (annual_salary)
2. The percentage of salary to be saved (portion_saved)
3. The cost of your dream home (total_cost)
4. The semi­annual salary raise (semi_annual_raise)

Test Case 1
>>>
Enter your starting annual salary:​ 120000
Enter the percent of your salary to save, as a decimal: . ​ 05
Enter the cost of your dream home: ​500000
Enter the semi­annual raise, as a decimal:​ .03
Number of months:​ 142
>>>
Test Case 2
>>>
Enter your starting annual salary:​ 80000
Enter the percent of your salary to save, as a decimal: . ​ 1
Enter the cost of your dream home: ​800000
Enter the semi­annual raise, as a decimal:​ .03
Number of months:​ 159
>>>
Test Case 3
>>>
Enter your starting annual salary:​ 75000
Enter the percent of your salary to save, as a decimal: . ​ 05
Enter the cost of your dream home:​ 1500000
Enter the semi­annual raise, as a decimal:​ .05
Number of months:​ 261
>>>
'''