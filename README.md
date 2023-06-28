# sqlalchemy-challange

## Hawaii Climate Analysis/App

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area.

## Climate Data Analysis

- Gets the most recent date of the dataset given and gets the previous years worth of precipitation data in Hawaii
- Creates a graph showing the precipitaion by each date
- Gets the most active station in Hawaii
- Creates a graph showing the temperature oberservation of the most active station in Hawaii

## Climate App

Running and following the app.py file creates an app in a browser. Below is a description of each route in the app:

 ------------------------------------------------------------------------------------------------------------------

precipitation: returns a dictionary with a date as the key and the value as the precipitation within the last year

stations: returns a json of all the stations in the data

tobs: returns a json on the last years data for the most active station

start: returns the min, avg, and max values of a given date until the most recent date

start/end: returns the min, avg, max values of a range set by the url
