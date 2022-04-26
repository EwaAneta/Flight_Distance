import pandas as pd
from numpy import cos, sin, arcsin, sqrt
from math import radians

#set amount of displayed df columns to 15
pd.set_option('display.max_columns', 15)
#set width of the terminal window to 1000
pd.options.display.width = 1000


def xlookup(lookup_value, lookup_array, return_array, if_not_found:str =''):
    """
    Searches a range or an array for a match and returns the coresponding item from a second range or array.

    Args:
    lookup_value: the value we are interested, this will be a string value
    lookup_array: this is a column inside the source pandas dataframe, we are looking for the “lookup_value” inside this array/column
    return_array: this is a column inside the source pandas dataframe, we want to return values from this column
    if_not_found: will be returned if the “lookup_value” is not found

    Returns:
    match_value[]: list with the values based on lookup values

    Source: https://pythoninoffice.com/replicate-excel-vlookup-hlookup-xlookup-in-python

    """
    match_value = return_array.loc[lookup_array==lookup_value]
    if match_value.empty:
        return f'"{lookup_value}" not found!' if if_not_found == '' else if_not_found
    else:
        return match_value.tolist()[0]


flight_distance_csv = 'FlightDistanceTest.csv'
airport_codes_iata_csv = 'airport_codes_iata.csv'

# load data files into dataframes
df_flight_csv = pd.read_csv(flight_distance_csv, encoding = 'utf-8-sig')
df_airport_codes_csv = pd.read_csv(airport_codes_iata_csv, encoding = 'utf-8-sig')

# use xlookup function to get actual departure and arrival municipality names, country codes
df_flight_csv['Verified Departure City and Country'] = df_flight_csv['Departure Code'].apply(xlookup, args = (df_airport_codes_csv['iata_code'],df_airport_codes_csv['municipality']))
df_flight_csv['Verified Departure Country Code'] = df_flight_csv['Departure Code'].apply(xlookup, args = (df_airport_codes_csv['iata_code'],df_airport_codes_csv['iso_country']))
df_flight_csv['Verified Departure City and Country'] = df_flight_csv['Verified Departure City and Country'].str.cat(df_flight_csv['Verified Departure Country Code'], sep = ', ')
del df_flight_csv['Verified Departure Country Code']

df_flight_csv['Verified Arrival City and Country'] = df_flight_csv['Arrival Code'].apply(xlookup, args = (df_airport_codes_csv['iata_code'],df_airport_codes_csv['municipality']))
df_flight_csv['Verified Arrival Country Code'] = df_flight_csv['Arrival Code'].apply(xlookup, args = (df_airport_codes_csv['iata_code'],df_airport_codes_csv['iso_country']))
df_flight_csv['Verified Arrival City and Country'] = df_flight_csv['Verified Arrival City and Country'].str.cat(df_flight_csv['Verified Arrival Country Code'], sep = ', ')
del df_flight_csv['Verified Arrival Country Code']

# concatenate columns of a dataframe
df_flight_csv['Verified City Pair'] = df_flight_csv['Verified Departure City and Country'].str.cat(df_flight_csv['Verified Arrival City and Country'], sep = ' - ')

del df_flight_csv['Verified Departure City and Country']
del df_flight_csv['Verified Arrival City and Country']

# use xlookup function to get actual departure coordinates
df_flight_csv['Verified_dep_coordinates'] = df_flight_csv['Departure Code'].apply(xlookup, args = (df_airport_codes_csv['iata_code'],df_airport_codes_csv['coordinates']))

# split actual departure coordinates into longitude and latitude
df_flight_csv[['Verified_dep_lon', 'Verified_dep_lat']] = df_flight_csv['Verified_dep_coordinates'].str.split(', ', 1, expand = True)
del df_flight_csv['Verified_dep_coordinates']

def check_numeric(x):
    """
    Converts argument to float if it is a number.

    Args:
    x: checked value

    Returns:
    True if value is numeric,
    False if value is not numeric.
    """
    try:
        float(x)
        return True
    except:
        return False

# check if 'Verified_dep_lon' is numeric and filters the row out if otherwise
df_flight_csv = df_flight_csv[df_flight_csv['Verified_dep_lon'].apply(check_numeric)]
df_flight_csv ['Verified_dep_lon'] = pd.to_numeric(df_flight_csv['Verified_dep_lon'])

# check if 'Verified_dep_lat' is numeric and filters the row out if otherwise
df_flight_csv = df_flight_csv[df_flight_csv['Verified_dep_lat'].apply(check_numeric)]
df_flight_csv ['Verified_dep_lat'] = pd.to_numeric(df_flight_csv['Verified_dep_lat'])

# use xlookup function to get actual arrival coordinates
df_flight_csv['Verified_arr_coordinates'] = df_flight_csv['Arrival Code'].apply(xlookup, args = (df_airport_codes_csv['iata_code'],df_airport_codes_csv['coordinates']))

# split actual arrival coordinates into longitude and latitude
df_flight_csv[['Verified_arr_lon', 'Verified_arr_lat']] = df_flight_csv['Verified_arr_coordinates'].str.split(', ', 1, expand = True)
del df_flight_csv['Verified_arr_coordinates']

# check if 'Verified_arr_lon' is numeric and filters the row out if otherwise
df_flight_csv = df_flight_csv[df_flight_csv['Verified_arr_lon'].apply(check_numeric)]
df_flight_csv ['Verified_arr_lon'] = pd.to_numeric(df_flight_csv['Verified_arr_lon'])

# check if 'Verified_arr_lat' is numeric and filters the row out if otherwise
df_flight_csv = df_flight_csv[df_flight_csv['Verified_arr_lat'].apply(check_numeric)]
df_flight_csv ['Verified_arr_lat'] = pd.to_numeric(df_flight_csv['Verified_arr_lat'])

# change order of columns in dataframe
df_flight_csv = df_flight_csv.reindex(columns = ['Normalised City Pair',
                                                 'Departure Code',
                                                 'Arrival Code',
                                                 'Departure_lat',
                                                 'Departure_lon',
                                                 'Arrival_lat',
                                                 'Arrival_lon',
                                                 'Verified City Pair',
                                                 'Verified_dep_lat',
                                                 'Verified_dep_lon',
                                                 'Verified_arr_lat',
                                                 'Verified_arr_lon'])

def original_haversine_distance(row):
    """
    Calculate the great circle distance between the two Earth coordinates (in nautical miles)
    from the original csv file, using haversine formula.

    Source: https://en.wikipedia.org/wiki/Haversine_formula

    Args:
    row: DataFrame row

    Returns:
    distance: distance between the two Earth coordinates (in nautical miles)
    """
    # assign departure longitude, specified in decimal degrees
    lon1 = row['Departure_lon']

    # assign departure latitude, specified in decimal degrees
    lat1 = row['Departure_lat']

    # assign arrival longitude, specified in decimal degrees
    lon2 = row['Arrival_lon']

    # assign arrival latitude, specified in decimal degrees
    lat2 = row['Arrival_lat']

    # specify Earth radius in nautical miles
    r = 3440

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # calculate latitude diference
    d_lat = lat2 - lat1

    # calculate longitude diference
    d_lon = lon2 - lon1

    # apply haversine Haversine_formula
    a = sin(d_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
    central_angle = 2 * arcsin(sqrt(a))
    distance = r * central_angle

    return distance

# apply original_haversine_distance function on all DataFrame rows to get distance between orginal airport coordinates in nautical miles
df_flight_csv['Declared_Distance_NM'] = df_flight_csv.apply(lambda row: original_haversine_distance(row), axis=1)

def verified_haversine_distance(row):
    """
    Calculate the great circle distance between the two Earth coordinates (in nautical miles)
    from the looked up actual coordinates from https://www.datahub.io/core/airport-codes#data for given aiports in original csv file, using haversine formula.

    Source: https://en.wikipedia.org/wiki/Haversine_formula

    Args:
    row: DataFrame row

    Returns:
    distance: distance between the two Earth coordinates (in nautical miles)
    """
    # assign departure longitude, specified in decimal degrees
    lon1 = row['Verified_dep_lon']

    # assign departure latitude, specified in decimal degrees
    lat1 = row['Verified_dep_lat']

    # assign arrival longitude, specified in decimal degrees
    lon2 = row['Verified_arr_lon']

    # assign arrival latitude, specified in decimal degrees
    lat2 = row['Verified_arr_lat']

    # specify Earth radius in nautical miles
    r = 3440

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # calculate latitude diference
    d_lat = lat2 - lat1

    # calculate longitude diference
    d_lon = lon2 - lon1

    # apply haversine Haversine_formula
    a = sin(d_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
    central_angle = 2 * arcsin(sqrt(a))
    distance = r * central_angle

    return distance

# apply verified_haversine_distance function on all DataFrame rows to get distance between verified airport coordinates in nautical miles
df_flight_csv['Verified_Distance_NM'] = df_flight_csv.apply(lambda row: verified_haversine_distance(row), axis=1)

# calculate absolute value of distance difference
df_flight_csv['Distance_difference'] = (df_flight_csv['Declared_Distance_NM'] - df_flight_csv['Verified_Distance_NM']).abs()

print(df_flight_csv)

# save dataframe to csv file
df_flight_csv.to_csv('FlightDistanceTest_Python.csv', encoding = 'utf-8-sig')
