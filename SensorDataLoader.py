#SensorDataLoader.py
# This script is used to load sensor data from a CSV and json file.

import csv
import json

class SensorDataLoader:
    def __init__(self, sensor_csv=None, sensor_json=None):
        """
        Initialize the sensor data loader with CSV and JSON file paths.
        sensor_csv: Path to a CSV file containing sensor data.
        sensor_json: Path to a JSON file containing sensor data.
        """
        self.csv_data = []
        self.json_data = []

        if sensor_csv:
            self.load_csv(sensor_csv)
        if sensor_json:
            self.load_json(sensor_json)

    def load_csv(self, sensor_csv):
        """
        Load sensor data from a CSV file.
        sensor_csv: Path to a CSV file containing sensor data.
        CSV file should have columns "id", "latitude", and "longitude".
        """
        with open(sensor_csv, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row["id"] = int(row["id"])
                    row["latitude"] = float(row["latitude"])
                    row["longitude"] = float(row["longitude"])
                    self.csv_data.append(row)
                except ValueError:
                    print("Error: Unable to parse row:", row)

    def load_json(self, sensor_json):
        """
        Load sensor data from a JSON file.
        sensor_json: Path to a JSON file containing sensor data.
        JSON file should be a list of dictionaries with keys "id", "latitude", and "longitude".
        """
        with open(sensor_json, 'r') as file:
            try:
                data = json.load(file)
                for entry in data:
                    try:
                        entry["id"] = int(entry["id"])
                        entry["latitude"] = float(entry["latitude"])
                        entry["longitude"] = float(entry["longitude"])
                        self.json_data.append(entry)
                    except ValueError:
                        print("Error: Unable to parse entry:", entry)
            except json.JSONDecodeError:
                print("Error: Unable to decode JSON file:", sensor_json)

if __name__ == "__main__":
    csv_file = 'SensorData1.csv'
    json_file = 'SensorData2.json'
    initializer = SensorDataLoader(sensor_csv=csv_file, sensor_json=json_file)
    
    print("Loaded CSV data:")
    for data in initializer.csv_data:
        print(data)
    
    print("\nLoaded JSON data:")
    for data in initializer.json_data:
        print(data)


        