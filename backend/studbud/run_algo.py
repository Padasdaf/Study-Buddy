import time
import csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import matchingalgorithm
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import pairwise_distances
import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studbud.settings')
django.setup()

from studbud.import_cluster import import_top_users
from matchingalgorithm import generate_buddies, user_info, course_codes, features_to_scale, updateDB

# Define the CSV file path
csv_file_path = os.path.abspath('../generated_users.csv')  # Convert to absolute path

class CSVFileHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_modified_time = None  

    def on_modified(self, event):
    # Check if the modified file is the target CSV
    if os.path.abspath(event.src_path) == csv_file_path:
        print(f"Detected modification in {csv_file_path}")
        current_modified_time = os.path.getmtime(csv_file_path)

        if self.last_modified_time == current_modified_time:
            return  # Skip redundant updates
        self.last_modified_time = current_modified_time

        # Run the algorithm
        print("CSV file modified. Running the algorithm...")
        try:
            generate_buddies(user_info, course_codes, features_to_scale)
            updateDB()
            print("Algorithm successfully executed and database updated.")
        except Exception as e:
            print(f"Error during algorithm execution: {e}")

observer = Observer()
event_handler = CSVFileHandler()

observer.schedule(event_handler, path=os.path.dirname(csv_file_path), recursive=False)
observer.start()

try:
    print("Monitoring started. Press Ctrl+C to stop.")
    while True:
        time.sleep(1)  # Keep the program running
except KeyboardInterrupt:
    print("Monitoring stopped.")
    observer.stop()

observer.join()
