#!/usr/bin/env python3
# main.py
# Main class: load sensor data from CSV and JSON files, create a spatial index, and find the closest sensor points within a 100m radius. and create a mapping between csv sensor IDs and json sensor IDs.
# author: Hyunmyung Park
# 2025/03/11

import json
import SensorDataLoader
import SpatialIndexer
import numpy as np

class Main:
    def __init__(self, csv_file, json_file):
        """
        Initialize the main application with CSV and JSON file paths.
        csv_file: Path to a CSV file containing sensor data.
        json_file: Path to a JSON file containing sensor data.
        """
        self.csv_file = csv_file
        self.json_file = json_file

    def run(self):
        # use SensorDataLoader to load sensor data from CSV and JSON files
        sensor_loader = SensorDataLoader.SensorDataLoader(sensor_csv=self.csv_file, sensor_json=self.json_file)
        print("CSV sensor data loaded:", len(sensor_loader.csv_data))
        print("JSON sensor data loaded:", len(sensor_loader.json_data))
        
        # create a spatial index using the CSV sensor data
        indexer = SpatialIndexer.SpatialIndexer(sensor_loader.csv_data)
        
        # find the closest sensor points within a 100m radius of each JSON sensor point
        # and create a mapping between csv sensor IDs and json sensor IDs 
        radius_m = 100  # 100 m
        radius_rad = radius_m / 6371000  # m to radians (Earth's average radius: 6,371,000 m)
        mapping = {}  # mapping between json sensor IDs and csv sensor IDs

        for point in sensor_loader.json_data:
            query_point = (point["latitude"], point["longitude"])
            # query the spatial index for sensor data points within a 100m radius
            query_point_rad = np.radians([query_point])
            dist, ind = indexer.tree.query(query_point_rad, k=1)
            if dist[0][0] <= radius_rad:
                # get the CSV sensor data for the closest point
                csv_sensor = sensor_loader.csv_data[ind[0][0]]
                # create a mapping between the JSON sensor ID and CSV sensor ID
                mapping[csv_sensor["id"]] = str(point["id"])

        # print the mapping between json sensor IDs and csv sensor IDs
        print(json.dumps(mapping, indent=4))

        # create output file for the mapping
        with open("sensor_mapping.json", "w") as outfile:
            json.dump(mapping, outfile, indent=4)


if __name__ == "__main__":
    # run the main application with the CSV and JSON file paths
    csv_file = "SensorData1.csv"
    json_file = "SensorData2.json"
    main_app = Main(csv_file, json_file)
    main_app.run()
