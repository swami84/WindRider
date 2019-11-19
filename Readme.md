# WindRider

## Predictive Insights from Ridesharing Analytics

- Over the recent years, there has been an increased demand for ride sharing services both within domestic US and globally

- Currently there are more than 67,000 active drivers who provide ride sharing service in the city of Chicago[1]

- Popular ride sharing service providers such as Lyft and Uber are yet to generate positive cash flow

- In order to retain and grow daily/monthly active customers, ride sharing services need to be cost (time and fare) competitive with other services (bike rental and Metro)

- To gain a competitive edge ride sharing services need to retain and scale their customer base (both riders and drivers)

#### My capstone project, WindRider, aims to solve some of these issues by highlighting the important features and providing accurate trip information to the ride share customers.

For my analysis, I used Chicago city's rideshare network data. The city of Chicago has released uncorrelated anonymous datasets on

- [Drivers](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Drivers/j6wf-834c) (Residence Zip Code, Start Date, Reported Date, Number of Trips)

- [Vehicles](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Vehicles/bc6b-sq4u) (Make, Model, Year, Number of Trips, Inspection Month)

- [Trips](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips/m6dm-c72p) (Pickup location, Time, Dropoff Location, Time, Trip Time, Trip Distance, Trip Fare)

# Brief Insights
## Proximity Effect:

- Drivers who reside closer to Chicago city center (proximity) have higher throughput (trips/unit time)

![Image 2](https://github.com/swami84/WindRider/blob/master/Notebooks/Images/Driver_Num_Trips_Zip%20Code%20Map.png)

- Proximity effect amplifies over the years

![Image 1](https://github.com/swami84/WindRider/blob/master/Notebooks/Images/Distance%20vs%20Trip%20Per%20Year.png)

## Temporal Trip Trends

- Most rides and ride cost peak between 4 - 8 PM

![Image 3](https://github.com/swami84/WindRider/blob/master/Notebooks/Images/Trips_Week_Summary.png)




## Top 15 Vehicles

- Graph shows the top 15 vehicles by avg number of trips
![Image 4](https://github.com/swami84/WindRider/blob/master/Notebooks/Images/Top%2015%20Vehicles.png)

# Conclusions

- ### City of Chicago’s rideshare network’s drivers data was analyzed
```
	-Over the years rideshare drivers network have expanded to suburbs of the city

	-Drivers residing closer to Chicago city were able to provide more rides compared to drivers residing farther from the city

	-Mean Rides/Driver/Year dropped by ~ 1.5 rides for every residence mile away from city center
```
* ### A brief analysis of the rider and trip trends shows
```
	-Downtown Chicago is the most active area for pickup and drop-offs at most times

	-Passengers from northern suburbs request more pickups to downtown in the morning and vice versa in the evenings

	-Friday and Saturday night trip count dominate among other weekdays, Trip rates are highest during peak pickup time (8-10AM, 4-6PM)

	-Monthly trip analysis shows number of trips for winter months is higher compared to other months trip cost ($/mile) is highest for summer month
```
* ###  Two prediction models – Ridge & Random Forest were utilized to predict trip cost and time
```
	-Important features in order – Trip Miles, Distance from City Center, Carpool and pick up hour
```

# Further Reading
- All analysis and predictive models can be found in the [Notebooks](https://github.com/swami84/WindRider/tree/master/Notebooks) folder
- Images can be found in [Images](https://github.com/swami84/WindRider/tree/master/Notebooks/Images) folder
- Spatio - Temporal Maps are located in [HTML](https://github.com/swami84/WindRider/tree/master/Notebooks/HTML) folder
