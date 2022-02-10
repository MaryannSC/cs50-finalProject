from helpers import convert_to_yards, convert_to_meters, convert_to_miles

monthlyTotals = [{'year': '2021', 'month': '12', 'SUM(distance)': 3000.0, 'units': 'meters'},
                {'year': '2021', 'month': '12', 'SUM(distance)': 11000.0, 'units': 'yards'},
                {'year': '2021', 'month': '11', 'SUM(distance)': 3000.0, 'units': 'meters'},
                {'year': '2021', 'month': '11', 'SUM(distance)': 2.0, 'units': 'miles'},
                {'year': '2021', 'month': '11', 'SUM(distance)': 10000.0, 'units': 'yards'},
                {'year': '2021', 'month': '10', 'SUM(distance)': 6000.0, 'units': 'meters'},
                {'year': '2021', 'month': '10', 'SUM(distance)': 2.0, 'units': 'miles'},
                {'year': '2021', 'month': '10', 'SUM(distance)': 7650.0, 'units': 'yards'},
                {'year': '2021', 'month': '09', 'SUM(distance)': 6000.0, 'units': 'meters'},
                {'year': '2021', 'month': '09', 'SUM(distance)': 4.0, 'units': 'miles'},
                {'year': '2021', 'month': '09', 'SUM(distance)': 6300.0, 'units': 'yards'},
                {'year': '2020', 'month': '12', 'SUM(distance)': 3000.0, 'units': 'meters'},
                {'year': '2020', 'month': '12', 'SUM(distance)': 3000.0, 'units': 'yards'}]

# Determine which years are in database
allYears = []
for row in monthlyTotals:
    if row['year'] not in allYears:
        allYears.append(row['year'])

print("Years in log: {}".format(allYears))

# For each year determine how many months have data
hasData = {}
for y in allYears:
    allMonths = []
    for row in monthlyTotals:
        if row['year'] == y:
            if row['month'] not in allMonths:
                allMonths.append(row['month'])
                hasData[y] = allMonths

print("hasData = {}".format(hasData))



