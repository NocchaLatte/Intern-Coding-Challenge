# CUAVs-Coding-Challenge

Challenge Overview:

At Canadian UAVs, we handle large amounts of geospatial data, which is the focus of this challenge. The task involves correlating data from two sensors that detect anomalies. However, the sensors are not highly accurate, resulting in false positives and variations in their location readings. Your challenge is to associate the sensor readings based on their coordinates to identify common signals that may have been detected by both sensors. This correlation increases the likelihood that the signal is a genuine detection rather than a false positive.

Input Data:

The two sensors provide different output formats: one sensor outputs data in CSV format, and the other outputs data in JSON format. Please refer to the sample data for the exact format of each sensor's output. Both sensors assign a unique ID to each reading, but note that different sensors may use the same IDs. The sensor readings include location coordinates in decimal degrees, using the WGS 84 format, representing where the anomaly was detected. The sensors have an accuracy of 100 meters, meaning that the reported location is within 100 meters of the actual anomaly location.

Output:

The output should consist of pairs of IDs, where one ID is from the first sensor, and the second ID is from the second sensor.
# Sensor Data Correlation Challenge

## Overview

This project addresses the challenge of correlating sensor data from two different sources, each with a 100-meter uncertainty in their reported locations. One sensor provides data in CSV format and the other in JSON format. The goal is to determine if two sensor readings overlap within a specified radius, which increases the confidence that a signal is a genuine detection.

## Solution Approach

1. **Data Loading:**
   - **SensorDataLoader Class:**  
     The solution begins by loading sensor data from both CSV and JSON files. The `SensorDataLoader` class reads the CSV file using Python's `csv` module and the JSON file using the `json` module. It ensures that each record is correctly parsed and converts the sensor IDs, latitudes, and longitudes to their proper data types.

2. **Spatial Index Construction:**
   - **SpatialIndexer Class:**  
     To efficiently search for sensor readings within a given radius, the CSV sensor data is used to build a spatial index with a BallTree from scikit-learn.
     - The coordinates are converted from degrees to radians.
     - The BallTree is constructed using the haversine metric to calculate great-circle distances on the Earth's surface.
     - The `query_radius` method enables fast lookups for all points within a specified radius (converted from meters to radians).

3. **Mapping & Querying:**
   - **Main Class:**  
     The main workflow integrates both classes:
     - It loads sensor data via `SensorDataLoader`.
     - It builds a spatial index from the CSV data using `SpatialIndexer`.
     - For each sensor reading from the JSON data, the closest matching CSV reading is found within a 100-meter radius.
     - If a match is found, the JSON sensor's ID is mapped to the corresponding CSV sensor's ID.
     - The final output is a JSON-formatted mapping (e.g., `{"56": 46, "24": 74}`).

4. **Time and Space Complexity:**
   - **Time Complexity:**  
     - Data loading is \(O(N + M)\) where \(N\) is the number of CSV records and \(M\) is the number of JSON records.
     - Building the BallTree takes \(O(N \log N)\) time.
     - Each query for \(M\) points takes \(O(\log N)\) time on average, for a total of \(O(M \log N)\).
   - **Space Complexity:**  
     - The overall space requirement is \(O(N + M)\) to store the sensor data and the spatial index.

## Directory Structure

    /project-root
    │
    ├── SensorData1.csv          # CSV file with sensor data.
    ├── SensorData2.json         # JSON file with sensor data.
    ├── SensorDataLoader.py      # Module to load sensor data from files.
    ├── SpatialIndexer.py        # Module for building a spatial index using BallTree.
    └── main.py                  # Main script to run the sensor data correlation.

## How to Run

1. **Clone the repository and navigate to the project directory:**
   ```bash
   git clone https://github.com/NocchaLatte/Intern-Coding-Challenge.git
   cd [project-directory]
   ```
1. **Ensure you have the necessary dependencies installed (e.g., numpy, scikit-learn):**
    ```bash
    pip install numpy scikit-learn
    ```
1. **Run the main script:**    
    ```bash
    python main.py
    ```
    The script will load the sensor data, build the spatial index, and print out a JSON-formatted mapping that shows which JSON sensor readings have a corresponding CSV sensor reading within a 100-meter radius.
## Author
Hyunmyung Park
2025/03/11