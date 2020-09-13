# Finding the right amount to save away

def final_savings(starting_salary, portion_saved, semi_annual_raise = .07, r = .04, months = 36):
    """Return the amounts of money saved over a specified period."""
    
    annual_salary = starting_salary
    current_savings = 0
    for month in range(months):
        if(month + 1) % 6 == 0:
            annual_salary += semi_annual_raise * annual_salary
        current_savings += r / 12 * current_savings + (portion_saved / 10000) * annual_salary / 12
    
    return current_savings
    

def savings_rate(starting_salary, semi_annual_raise = .07, r = .04, months =36, portion_down_payment = .25, total_cost = 1000000):
    """Return the best rate of savings using bisection search."""
    
    down_payment = portion_down_payment * total_cost
    low = 0
    high = 10000
    portion_saved = (low + high) / 2
    epsilon = 100
    tries = 0
    
    # Check if reaching target is possible
    if final_savings(starting_salary, 10000) < down_payment:
        return False, None, None
    
    # Case if possible
    while abs(final_savings(starting_salary, portion_saved) - down_payment) > epsilon:
        
        if final_savings(starting_salary, portion_saved) < down_payment:
            low = portion_saved
        else:
            high = portion_saved
        
        portion_saved = int((low + high) / 2)
        tries += 1
    
    return True, portion_saved, tries
    

starting_salary = float(input("Enter the starting salary: "))
possible, portion_saved, tries = savings_rate(starting_salary)

if possible:
    print(f"Best savings rate: {portion_saved / 10000:.4f}")
    print(f"Steps in bisection search: {tries}")
else:
    print('It is not possible to pay the down payment in three years.')





























'''
To simplify things, assume:
1. Your semi­annual raise is .07 (7%)
2. Your investments have an annual return of 0.04 (4%)
3. The down payment is 0.25 (25%) of the cost of the house
4. The cost of the house that you are saving for is $1M.

You are now going to try to find the best rate of savings to achieve a down payment on a $1M house in
36 months. Since hitting this exactly is a challenge, we simply want your savings to be within $100 of
the required down payment.

In​ ps1c.py​, write a program to calculate the best savings rate, as a function of your starting salary.
You should use ​bisection search​ to help you do this efficiently. You should keep track of the number of
steps it takes your bisections search to finish. You should be able to reuse some of the code you wrote
for part B in this problem

Test Case 1
>>>
Enter the starting salary:​ 150000
Best savings rate:​ 0.4411
Steps in bisection search:​ 12
>>>
Test Case 2
>>>
Enter the starting salary:​ 300000
Best savings rate:​ 0.2206
Steps in bisection search:​ 9
>>>
Test Case 3
>>>
Enter the starting salary:​ 10000
It is not possible to pay the down payment in three years.
>>>

'''