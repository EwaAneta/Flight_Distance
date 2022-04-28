<**Flight_Distance**: Business trips are an integral part of work in many organizations. Many people, apart from short internal trips, are obliged to leave the country
even for a few days. Some companies sign contracts with airlines in order to receive better prices conditions.

A client who makes use of services of contracted airlines would like to know if the tracks of travel from the point-to-point mileage between their top destinations concur
with the mileage given by the carriers.

### Date created
Project: 1<sup>st</sup> March 2022

README: 27<sup>th</sup> April 2022

### Project Title
Flight Distance

### Description
This project uses data provided by contracted airlines and csv file contains airports IATA codes in order to establish the point-to-point distance between each of the airports given. The Flight Distance app calculates these distances using the longitude and latitude of locations wrapped into a function and compares them with the carrier-provided distances and gives a result which is the difference between the distance provided by carriers and the real distance.

The code provides the following information:

1.	**Gives actual departure and arrival municipality names, country codes**
2.	**Gives actual departure and arrival municipality names, country codes**
3.	**Gives actual departure and arrival coordinates**
4.	**Calculates the great circle distance between the two Earth coordinates (in nautical miles) from the original csv file, using haversine formula.**
5.	**Calculates the great circle distance between the two Earth coordinates (in nautical miles) from the looked up actual coordinates.**
6.	**Calculates an absolute value of the difference between the declared and actual distances.**
7.	**Saves DataFrame with all the information to a csv file.**

### Files used
    * FlightDistanceTest.csv (data provided by carriers)
    * airport_codes_iata.csv (file downloaded from website)



### Credits
During writing my "Flight_Distance " program I referred to these websites:

[IATA aiports codes.csv](https://www.datahub.io/core/airport-codes#data)
[Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula)
[Information on how to calculate the distance between two geolocations in Python](https://towardsdatascience.com/heres-how-to-calculate-distance-between-2-geolocations-in-python-93ecab5bbba4)
[Vectorised Haversine formula with a pandas dataframe](https://stackoverflow.com/questions/25767596/vectorised-haversine-formula-with-a-pandas-dataframe)
[Earth radius to Nautical miles Conversion - Length Measurement](https://trustconverter.com/en/length-conversion/earth-radius/earth-radius-to-nautical-miles.html)
[Pandas .str.isnumeric() for floats](https://stackoverflow.com/questions/68239333/pandas-str-isnumeric-for-floats)
[Replicate Excel VLOOKUP, HLOOKUP, XLOOKUP in Python](https://pythoninoffice.com/replicate-excel-vlookup-hlookup-xlookup-in-python/)
