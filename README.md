*Last Edited: 10/20/2021*

# Xtern-Work-Sample-Assesment
This repository contains my solution for XTERN Work Sample Assessment for summer 2022:
Important files:
* **Generated dataset** in the Dataset directory/folder
* **10 weeks of events**: A sample schedule for events in the span of 10 weeks
* **Python code** under the name *dataset_generator.py* that generated the dataset

P.S. The code is yet to be documented properly and optimized for best performance

# Objective
Main Goal: Generate a dataset to help you find the most convenient coworking places out of 5 potential locations.
Input: the location of the five workspace places and the location of the housing area.
Output: Return the best coworking place out of the five.

# Tools:
* 1- Python Programming Language
* 2- Google Maps API
* 3- Pandas library

# Approach:
Created a panadas data frame to serve as the dataset that contains all related data.
Filled the dataset with data (location, distance from housing place, number of restaurants nearby, etc...)
Evaluated each location based on the collected data giving each location an overall score out of 3.

# Evaluation Metrics:
The scoring metric grades are based on how close that location was to the ideal case and worst case. The closer the location was to the ideal case, the closer the score is to 1, and the closer it is to the worst case the closer to 0.

## Explaining each grading criteria for each attribute:
### Distance From Housing:
Ideal case: 5 minutes away (driving)
Worst case: 35 minutes away (driving)

The location gets 0 out of 1 if it was 35 minutes or more away from the housing area.

Nobody wants to be far away from their workplace, especially if they were in a big city such as Indianapolis where it is really easy for roads to get jammed.

### Number of Nearby Restaurants:
Ideal case: 20 or more restaurants near the coworking place
Worst case: 0 restaurants near the coworking place

This attribute is linear so I saw that it is better to just measure that. The quality of the food is very subjective so I decided not to include that complication in my calculations.
The attribute values for this attribute are the number of restaurants around the coworking location **within walking distance** (400 meters radius).

### Number of Nearby Events:
Ideal case: 20 or more events near the coworking place
Worst case: 0 restaurants near the coworking place

Just like the previous attribute, this one is linear since it measures the number of events around the coworking location and **within driving distance** (2.5 kilometers radius). Of course, there are all kinds of events and they are subjective as well, so I only included their number regardless of how appealing they were to me.

# Best Coworking location?
The best coworking location was the location with the least commute time from the housing place, +20 restaurants around it, +20 events around it...
It is none other than **Industrious Mass Ave** with an overall score of 2.99/3.
