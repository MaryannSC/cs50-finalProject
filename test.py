def convert_to_miles(totals):
    """ Converts distances in meters and yards to miles, adds entry already in miles and returns total value.

    Input:
    called from index()
    get user's distance totals by units from data base:
    totals = db.execute("SELECT units, SUM(distance) FROM swims WHERE userid=? GROUP BY units ORDER BY SUM(distance) DESC", session["user_id"])
    SUM(distance) is converted to float and stored as 'distance' in dict

    example input to function:
    totals = [{'units': 'yards', 'SUM(distance)': 14550.0, 'distance': 14550.0}, {'units': 'meters', 'SUM(distance)': 4000.0, 'distance': 4000.0},
              {'units': 'miles', 'SUM(distance)': 2.0, 'distance': 2.0}]

    output:
    4000.0 meters = 2.485484768949336 miles
    2.0 miles
    11450.0 yards = 6.505681818181818 miles
    Total in miles = 10.991166587131154

    """

    total_miles = 0

    for total in totals:
        # yards / 1760
        if total['units'] == 'yards':
            yards = total['distance'] / 1760.0
            total_miles = total_miles + yards
            print('{} yards = {} miles'.format(total['distance'], yards))

        # meters / 1609.344
        elif total['units'] == 'meters':
            meters = total['distance'] / 1609.344
            total_miles = total_miles + meters
            print('{} meters = {} miles'.format(total['distance'], meters))

        else:
            total_miles = total_miles + total['distance']
            print('{} miles'.format(total['distance']))

    return total_miles

def convert_to_meters(totals):
    """ Converts distances in yards and miles to meters, adds entry already in meters and returns total value.

    Input:
    called from index()
    get user's distance totals by units from data base:
    totals = db.execute("SELECT units, SUM(distance) FROM swims WHERE userid=? GROUP BY units ORDER BY SUM(distance) DESC", session["user_id"])
    SUM(distance) is converted to float and stored as 'distance' in dict

    example input to function:
    totals = [{'units': 'yards', 'SUM(distance)': 14550.0, 'distance': 14550.0}, {'units': 'meters', 'SUM(distance)': 4000.0, 'distance': 4000.0},
              {'units': 'miles', 'SUM(distance)': 2.0, 'distance': 2.0}]

    output:
    4000.0 meters
    2.0 miles = 3218.688 meters
    11450.0 yards = 10469.88 meters
    Total in meters = 17688.568

    """

    total_meters = 0

    for total in totals:
        if total['units'] == 'yards':
        # yards * .9144
            yards = total['distance'] * 0.9144
            total_meters = total_meters + yards
            print('{} yards = {} meters'.format(total['distance'], yards))

        # miles * 1609.344
        elif total['units'] == 'miles':
            miles = total['distance'] * 1609.344
            total_meters = total_meters + miles
            print('{} miles = {} meters'.format(total['distance'], miles))

        # already meters
        else:
            total_meters = total_meters + total['distance']
            print('{} meters'.format(total['distance']))

    return total_meters



def convert_to_yards(totals):
    """ Converts distances in meters and miles to yards, adds entry already in yards and returns total value.

    Input:
    called from index()
    get user's distance totals by units from data base:
    totals = db.execute("SELECT units, SUM(distance) FROM swims WHERE userid=? GROUP BY units ORDER BY SUM(distance) DESC", session["user_id"])
    SUM(distance) is converted to float and stored as 'distance' in dict

    example input to function:
    totals = [{'units': 'yards', 'SUM(distance)': 14550.0, 'distance': 14550.0}, {'units': 'meters', 'SUM(distance)': 4000.0, 'distance': 4000.0},
              {'units': 'miles', 'SUM(distance)': 2.0, 'distance': 2.0}]

    output:
    4000.0 meters = 4374.4532 yards
    2.0 miles = 3520.0 yards
    11450.0 yards
    Total in yards = 19344.4532

    """

    total_yards = 0

    for total in totals:
        if total['units'] == 'meters':
        # meters * 1.0936133
            meters = total['distance'] * 1.0936133
            print('{} meters = {} yards'.format(total['distance'], meters))
            total_yards = total_yards + meters

        # miles * 1760
        elif total['units'] == 'miles':
            miles = total['distance'] * 1760.0
            print('{} miles = {} yards'.format(total['distance'], miles))
            total_yards = total_yards + miles

        # already yards
        else:
            print('{} yards'.format(total['distance']))
            total_yards = total_yards + total['distance']

    return total_yards

########################################
# from database
totals = [{'units': 'meters', 'SUM(distance)': 4000.0}, {'units': 'miles', 'SUM(distance)': 2.0}, {'units': 'yards', 'SUM(distance)': 11450.0}]

# add float distance to dict
for total in totals:
    total['distance'] = float(total['SUM(distance)'])
    print ('Units: {}   Distance: {}'.format(total['units'], total['distance']))

print('Total in yards = {}'.format(convert_to_yards(totals)))
print('Total in meters = {}'.format(convert_to_meters(totals)))
print('Total in miles = {}'.format(convert_to_miles(totals)))



