import csv
import pandas as pd
from pandas.core.frame import DataFrame
import googlemaps
import time
import math

with open(r"C:\Users\Ahmed Alghafri\Documents\Google_API_KEY.txt") as f:
    API_KEY = f.readline()


# https://googlemaps.github.io/google-maps-services-python/docs/
gmaps = googlemaps.Client(key=API_KEY)


col_num = 0
df = pd.read_csv("workspace locations.csv")


dataset = DataFrame()

# distance to work place
# number of restaurants around the area within walking distance
# number of events around the working space within driving distance



# Adding names of workplaces
dataset.insert(col_num, df.columns[col_num], df[df.columns[0]][1:])
col_num += 1

# Adding the addresses
locations = [df[df.columns[col_num]][i+1] for i in range(len(df.columns[col_num])-2)]
dataset.insert(col_num, df.columns[col_num], locations)
col_num += 1

# Add distance from housing place to each coworking place
addresses = list(df[df.columns[1]][1:])
lat_long_lst = []

for i in addresses:
    result = gmaps.geocode(i)
    lat = result[0]['geometry']['location'] ['lat']
    lon = result[0]['geometry']['location'] ['lng']
    lat_long_lst.append((lat, lon))
    time.sleep(1)
dataset.insert(col_num, 'Latitude & Longitude', lat_long_lst)
col_num += 1



# Calculate distances 
result = gmaps.geocode(df["Address"][0])
from_lat = result[0]['geometry']['location'] ['lat']
from_lng = result[0]['geometry']['location'] ['lng']

distances = []

for i in range(1, len(dataset['Latitude & Longitude'])+1):
    to_lat, to_lng = dataset['Latitude & Longitude'][i]
    dis = gmaps.distance_matrix([str(from_lat) + " " + str(from_lng)], [str(to_lat) + " " + str(to_lng)], mode='driving')
    distances.append(round(dis['rows'][0]['elements'][0]['duration']['value']/60, 2))
dataset.insert(col_num, 'Distance From Housing', distances)
col_num += 1



# Find number of restaurants nearby
# must be within walking distance
nearby_restaurant = {}
num_of_restaurants = []
for i in range(1, len(dataset['Latitude & Longitude'])+1):
    restaurants_nearby_result = gmaps.places_nearby(
        location= dataset['Latitude & Longitude'][i],
        keyword= "restaurant",
        type= "restaurant",
        radius=400,
        max_price=3,
    )
    temp_lst = []
    for x in restaurants_nearby_result.get("results"):
        temp_lst.append(x['name'])

    nearby_restaurant[df[df.columns[0]][i]] = temp_lst
    num_of_restaurants.append(len(restaurants_nearby_result.get("results")))

dataset.insert(col_num, '# of Nearby Restaurants', num_of_restaurants)
col_num += 1


# save restaurants!
with open(r"Suplemental CSVs\Nearby Restaurants.csv", 'w') as f:
    writ = csv.writer(f)
    for key, value in nearby_restaurant.items():
        writ.writerow([key, value, len(value)])

# Find number of events nearby
# must be within driving distance
nearby_events = {}
num_of_events = []
for i in range(1, len(dataset['Latitude & Longitude'])+1):
    events_nearby_result = gmaps.places_nearby(
        location= dataset['Latitude & Longitude'][i],
        keyword= "event",
        type= "event",
        radius=2500,
    )
    temp_lst = []
    for x in events_nearby_result.get("results"):
        temp_lst.append(x['name'])

    nearby_events[df[df.columns[0]][i]] = temp_lst
    num_of_events.append(len(events_nearby_result.get("results")))

dataset.insert(col_num, '# of Nearby Events', num_of_events)
col_num += 1

# save events!
with open(r"Suplemental CSVs\Nearby Events.csv", 'w') as f:
    writ = csv.writer(f)
    for key, value in nearby_events.items():
        writ.writerow([key, value, len(value)])


def sigmoid(x):
    return 1 /(1+(math.e)**-x)
def dist_to_score(t):
    # average distance being 20 minutes
    # best case being 5 minutes`
    return (20 - t)/2.5

def restaurant_to_score(x):
    return x/20
def events_to_score(x):
    return x/20

total = [0 for i in range(5)]

index = 0
for i in dataset['Distance From Housing']:
    total[index] += sigmoid(dist_to_score(i))
    index += 1

index = 0
for i in dataset['# of Nearby Restaurants']:
    total[index] += restaurant_to_score(i)
    index += 1
index = 0
for i in dataset['# of Nearby Events']:
    total[index] += events_to_score(i)
    total[index] = round(total[index], 2)
    index += 1


dataset.insert(col_num, 'Final Score', total)
col_num += 1

dataset.to_csv(r"Dataset/generated_dataset.csv", index=False, header=True)