distance = 2
units = 'miles'

yards = meters = miles = 0

# distance entered in yards
if units == 'yards':
    yards = distance
    miles = distance / 1760                 
    meters = distance * 0.9144               
    
# distance entered in meters
elif units == 'meters':
    meters = distance
    yards = distance / 0.9144          
    miles = distance / 1609.344             

# distance entered in miles
elif units == 'miles':
    miles = distance
    yards = distance * 1760                  
    meters = distance * 1609.344             



print ("yards = {}, meters = {}, miles = {}".format(yards, meters, miles))