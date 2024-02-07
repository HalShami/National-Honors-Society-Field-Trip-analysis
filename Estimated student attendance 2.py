import pandas as pd
from uszipcode import SearchEngine
from geopy.distance import geodesic

# Read the Excel file
file_path = 'NHS_survey_cleaned.xlsx'  # Replace 'NHS_survey_cleaned.xlsx' with the path to your Excel file
data = pd.read_excel(file_path)

# Calculate mean and median
mean_likelihood = data['Likeliness to Attend'].mean()
median_likelihood = data['Likeliness to Attend'].median()

# Round the mean to the nearest whole number
mean_rounded = round(mean_likelihood)

# Count the number of non-null values under the "Likeliness to Attend" column
num_values = data['Likeliness to Attend'].count()

# Estimate attendance
estimated_attendance = num_values * (mean_rounded / 10)

# Search for zip codes within 60-mile radius of the given zip code
search = SearchEngine()
zipcode_info = search.by_zipcode("72223")
base_coordinates = (zipcode_info.lat, zipcode_info.lng)

count_within_radius = 0
for index, row in data.iterrows():
    zipcode_info = search.by_zipcode(row['Zip Code'])
    if zipcode_info is not None and zipcode_info.lat is not None and zipcode_info.lng is not None:
        coordinates = (zipcode_info.lat, zipcode_info.lng)
        distance = geodesic(base_coordinates, coordinates).miles
        if distance <= 60:
            count_within_radius += 1

# Adjust estimated attendance based on zip codes within radius
adjusted_estimated_attendance = estimated_attendance * (count_within_radius / num_values)

print("Estimated attendance adjusted for zip codes within a 60-mile radius:", adjusted_estimated_attendance)
