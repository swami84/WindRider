# WindRider

## Predictive Insights from Ridesharing Analytics

- Over the recent years, there has been an increased demand for ride sharing services both within domestic US and globally

- Currently there are more than 67,000 active drivers who provide ride sharing service in the city of Chicago[1]

- Popular ride sharing service providers such as Lyft and Uber are yet to generate positive cash flow

- In order to retain and grow daily/monthly active customers, ride sharing services need to be cost (time and fare) competitive with other services (bike rental and Metro)

- To gain a competitive edge ride sharing services need to retain and scale their customer base (both riders and drivers)

The city of Chicago has released uncorrelated anonymous datasets on

- [Drivers](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Drivers/j6wf-834c) (Residence Zip Code, Start Date, Reported Date, Number of Trips)

- [Vehicles](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Vehicles/bc6b-sq4u) (Make, Model, Year, Number of Trips, Inspection Month)

- [Trips](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips/m6dm-c72p) (Pickup location, Time, Dropoff Location, Time, Trip Time, Trip Distance, Trip Fare)

Some key insights

# Proximity Effect:

- Drivers who reside closer to Chicago city center (proximity) have higher throughput (trips/unit time)

![Image 2](https://github.com/swami84/WindRider/blob/master/Notebooks/Images/Driver_Num_Trips_Zip%20Code%20Map.png)

- Proximity effect amplifies over the years

![Image 1](https://github.com/swami84/WindRider/blob/master/Notebooks/Images/Distance%20vs%20Trip%20Per%20Year.png)

# Temporal Trip Trends

- Most rides and ride cost peak between 4 - 8 PM

![Image 3](https://github.com/swami84/WindRider/blob/master/Notebooks/Images/Week_Summary.png)
