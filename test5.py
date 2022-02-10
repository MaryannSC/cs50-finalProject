from helpers import formatDistance

# get monthly totals
units = 'yards'

# command = "SELECT strftime('%Y', date) as year, strftime('%m', date) as month, SUM(" + units +") " \
#           "FROM swims WHERE userid=? GROUP BY year, month ORDER BY year DESC, month DESC"
# print(command)

# monthlyTotals = db.execute(command, session["user_id"])


# monthlyTotals = [{'year': '2021', 'month': '12', 'SUM(yards)': 12500.83989501312, 'distance': '12,500.84'}, {'year': '2021', 'month': '11', 'SUM(yards)': 10019.56255468066, 'distance': '10,019.56'}, {'year': '2021', 'month': '10', 'SUM(yards)': 7020.0, 'distance': '7,020.00'}, {'year': '2021', 'month': '09', 'SUM(yards)': 9800.83989501312, 'distance': '9,800.84'}, {'year': '2020', 'month': '12', 'SUM(yards)': 6280.839895013123, 'distance': '6,280.84'}, {'year': '2020', 'month': '11', 'SUM(yards)': 7020.0, 'distance': '7,020.00'}]

# cmd = "SUM(" + units + ")"

# for month in monthlyTotals:
#     month['distance'] = formatDistance(month[cmd])

# print(monthlyTotals)

# command = "SELECT strftime('%Y', date) as year, SUM(" + units + ") FROM swims WHERE userid=? " \
#           "GROUP BY year ORDER BY year DESC"

# print(command)

# yearTotals = db.execute(command, session["user_id"])


# for year in yearTotals:
#     year['distance'] = formatDistance(month[cmd])