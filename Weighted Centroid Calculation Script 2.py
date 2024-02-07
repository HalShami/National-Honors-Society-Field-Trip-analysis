from geopy.geocoders import Nominatim
import pandas as pd

# Load data from the spreadsheet
data = pd.read_excel("NHS_survey_cleaned.xlsx")  # Replace "your_file.xlsx" with your file path
zip_codes = data["Zip Code"].astype(str).tolist()  # Convert zip codes to strings
likeliness = data["Likeliness to Attend"].tolist()

# Initialize geolocator
geolocator = Nominatim(user_agent="meeting_locator")

# Function to get coordinates and weights (latitude, longitude, weight) from zip codes and likeliness
def get_coordinates_and_weights(zip_codes, likeliness):
    coordinates = []
    for i, zip_code in enumerate(zip_codes):
        location = geolocator.geocode(zip_code + ", USA")  # Adding ", USA" for specificity
        if location:
            coordinates.append((location.latitude, location.longitude, likeliness[i]))
    return coordinates

# Get coordinates and weights for all zip codes
coordinates_with_weights = get_coordinates_and_weights(zip_codes, likeliness)

# Calculate weighted centroid
total_weight = sum(weight for _, _, weight in coordinates_with_weights)
weighted_sum_latitude = sum(lat * weight for lat, lon, weight in coordinates_with_weights)
weighted_sum_longitude = sum(lon * weight for lat, lon, weight in coordinates_with_weights)

if total_weight > 0:
    centroid_latitude = weighted_sum_latitude / total_weight
    centroid_longitude = weighted_sum_longitude / total_weight

    print(f"The best meeting location's coordinates: Latitude {centroid_latitude}, Longitude {centroid_longitude}")
else:
    print("No valid coordinates found or total weight is zero.")