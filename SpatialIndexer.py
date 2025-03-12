# SpatialIndexer.py
# This script is used to create a spatial index for the data in the database.
# author:  Hyunmyung Park
# 2025/03/11

# initial idea
# since both sensor has 100m of uncertainty, we can draw a circle with 100m radius around the sensor location
# and then we can find the overlapping area of circle between two sensors

# from search, i found that we can use a balltree to make a spatial index
import numpy as np
from sklearn.neighbors import BallTree

class SpatialIndexer:
    def __init__(self, sensor_data):
        """
        Initialize the spatial indexer with sensor data.
        sensor_data: list of dictionaries, each with keys "id", "latitude", and "longitude".
        """
        self.sensor_data = sensor_data
        # Create a NumPy array of coordinates from sensor data (in degrees)
        self.coords = np.array([[entry["latitude"], entry["longitude"]] for entry in sensor_data])
        # Convert coordinates to radians for haversine metric calculations
        self.coords_rad = np.radians(self.coords)
        # Build the BallTree spatial index using the haversine metric
        self.tree = BallTree(self.coords_rad, metric='haversine')

    def query_radius(self, query_point, radius_m):
        """
        Query the spatial index for sensor data points within a given radius.
        query_point: tuple or list (latitude, longitude) in degrees.
        radius_m: radius in meters.
        Returns: Indices of sensor_data that fall within the given radius.
        """
        # Convert the query point from degrees to radians
        query_point_rad = np.radians([query_point])
        # Convert the search radius from meters to radians (using Earth's average radius of 6,371,000 m)
        radius_rad = radius_m / 6371000
        # Query the BallTree for indices within the specified radius
        indices = self.tree.query_radius(query_point_rad, r=radius_rad)
        return indices[0]  # Return the array of indices
    
if __name__ == "__main__":
    import SensorDataLoader
    sensor_loader = SensorDataLoader.SensorDataLoader(sensor_csv='SensorData1.csv', sensor_json='SensorData2.json')

    indexer = SpatialIndexer(sensor_loader.csv_data)

    # Example: Query using a sensor location with a 100m radius

    query_points = sensor_loader.json_data

    for point in query_points:
        print("Querying sensor data around point:", point)
        indices = indexer.query_radius((point["latitude"], point["longitude"]), radius_m=100)
        print("Found", len(indices), "sensor data points within 100m.")
        for idx in indices:
            print(sensor_loader.csv_data[idx])

