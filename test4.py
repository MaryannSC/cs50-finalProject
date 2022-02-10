monthlyTotals = [{'year': '2021', 'month': '12', 'SUM(yards)': 12500.83989501312},
                {'year': '2021', 'month': '11', 'SUM(yards)': 10019.56255468066},
                {'year': '2021', 'month': '10', 'SUM(yards)': 7020.0},
                {'year': '2021', 'month': '09', 'SUM(yards)': 9800.83989501312},
                {'year': '2020', 'month': '12', 'SUM(yards)': 6280.839895013123},
                {'year': '2020', 'month': '11', 'SUM(yards)': 7020.0}]
                
for month in monthlyTotals:
    month['distance'] = f"{month['SUM(yards)']:,.2f}"
    
print(monthlyTotals)    
    

'''
Output:
[{'year': '2021', 'month': '12', 'SUM(yards)': 12500.83989501312, 'distance': '12,500.84'}, 
{'year': '2021', 'month': '11', 'SUM(yards)': 10019.56255468066, 'distance': '10,019.56'}, 
{'year': '2021', 'month': '10', 'SUM(yards)': 7020.0, 'distance': '7,020.00'}, 
{'year': '2021', 'month': '09', 'SUM(yards)': 9800.83989501312, 'distance': '9,800.84'}, 
{'year': '2020', 'month': '12', 'SUM(yards)': 6280.839895013123, 'distance': '6,280.84'}, 
{'year': '2020', 'month': '11', 'SUM(yards)': 7020.0, 'distance': '7,020.00'}]                
'''

